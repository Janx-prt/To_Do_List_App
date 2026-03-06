from datetime import datetime, date
from sqlmodel import Session, select, func
from models import User, Todo, UserAchievement

LEVEL_THRESHOLDS = [0, 100, 250, 500, 800, 1200, 1700, 2300, 3000, 4000]

XP_BY_PRIORITY = {"Low": 10, "Medium": 25, "High": 50}
URGENT_BONUS = 15
EARLY_COMPLETION_BONUS = 10

ACHIEVEMENTS = {
    "first_quest": {"name": "First Quest", "description": "Complete your first todo", "icon": "🗡️"},
    "on_a_roll": {"name": "On A Roll", "description": "Complete 5 todos in a single day", "icon": "🔥"},
    "streak_master": {"name": "Streak Master", "description": "Maintain a 7-day streak", "icon": "⚡"},
    "speed_demon": {"name": "Speed Demon", "description": "Complete a todo before its due date", "icon": "💨"},
    "centurion": {"name": "Centurion", "description": "Complete 100 todos", "icon": "🏛️"},
    "perfectionist": {"name": "Perfectionist", "description": "Complete all todos in a category", "icon": "✨"},
    "high_roller": {"name": "High Roller", "description": "Complete 10 High priority todos", "icon": "🎰"},
}


def calc_level(xp: int) -> int:
    level = 1
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if xp >= threshold:
            level = i + 1
    return level


def calc_xp(todo: Todo) -> int:
    xp = XP_BY_PRIORITY.get(todo.priority, 10)
    if todo.category == "Urgent":
        xp += URGENT_BONUS
    if todo.due_date and todo.completed_at and todo.completed_at < todo.due_date:
        xp += EARLY_COMPLETION_BONUS
    return xp


def update_streak(user: User, completion_date: date):
    today_str = completion_date.isoformat()
    if user.last_completion_date:
        last = date.fromisoformat(user.last_completion_date)
        diff = (completion_date - last).days
        if diff == 1:
            user.current_streak += 1
        elif diff > 1:
            user.current_streak = 1
        # diff == 0 means same day, streak unchanged
    else:
        user.current_streak = 1
    user.last_completion_date = today_str
    if user.current_streak > user.max_streak:
        user.max_streak = user.current_streak


def check_achievements(session: Session, user: User, todo: Todo) -> list[str]:
    existing = session.exec(
        select(UserAchievement.achievement_key).where(UserAchievement.user_id == user.id)
    ).all()
    existing_set = set(existing)
    new_achievements = []

    # First Quest — 1 total completed
    if "first_quest" not in existing_set and user.total_completed >= 1:
        new_achievements.append("first_quest")

    # On A Roll — 5 completions today
    if "on_a_roll" not in existing_set:
        today_start = datetime.combine(date.today(), datetime.min.time())
        today_count = session.exec(
            select(func.count()).select_from(Todo).where(
                Todo.user_id == user.id,
                Todo.completed == True,
                Todo.completed_at >= today_start,
            )
        ).one()
        if today_count >= 5:
            new_achievements.append("on_a_roll")

    # Streak Master — 7-day streak
    if "streak_master" not in existing_set and user.current_streak >= 7:
        new_achievements.append("streak_master")

    # Speed Demon — completed before due date
    if "speed_demon" not in existing_set:
        if todo.due_date and todo.completed_at and todo.completed_at < todo.due_date:
            new_achievements.append("speed_demon")

    # Centurion — 100 total completed
    if "centurion" not in existing_set and user.total_completed >= 100:
        new_achievements.append("centurion")

    # Perfectionist — all todos in a category completed
    if "perfectionist" not in existing_set:
        cat_todos = session.exec(
            select(Todo).where(Todo.user_id == user.id, Todo.category == todo.category)
        ).all()
        if cat_todos and all(t.completed for t in cat_todos):
            new_achievements.append("perfectionist")

    # High Roller — 10 High priority todos completed
    if "high_roller" not in existing_set:
        high_count = session.exec(
            select(func.count()).select_from(Todo).where(
                Todo.user_id == user.id,
                Todo.completed == True,
                Todo.priority == "High",
            )
        ).one()
        if high_count >= 10:
            new_achievements.append("high_roller")

    # Save new achievements
    for key in new_achievements:
        session.add(UserAchievement(user_id=user.id, achievement_key=key))

    return new_achievements


def process_completion(session: Session, user: User, todo: Todo) -> dict:
    xp_earned = calc_xp(todo)
    old_level = user.level
    user.xp += xp_earned
    user.total_completed += 1
    user.level = calc_level(user.xp)

    update_streak(user, date.today())
    new_achievements = check_achievements(session, user, todo)

    level_up = user.level > old_level

    return {
        "xp_earned": xp_earned,
        "total_xp": user.xp,
        "level_up": level_up,
        "new_level": user.level,
        "new_achievements": [
            {**ACHIEVEMENTS[key], "key": key} for key in new_achievements
        ],
    }
