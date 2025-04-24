from pyscripts.wave_function.conflict import *
from pyscripts.week_generator import *
# from rich import print

# def get_min_entropy_position(week_program):
#     best_day = None
#     best_hour = None
#     best_entropy = None

#     for day in week_program:
#         for hour in week_program[day]:
#             hour_entropy = len(week_program[day][hour]["conflicts"])

#             if best_entropy is None or hour_entropy != 0 and hour_entropy < best_entropy:
#                 best_entropy = hour_entropy
#                 best_hour = hour
#                 best_day = day
    
#     return best_day, best_hour, best_entropy

def get_lecture_sorted_entropy_positions(
    lecture,
    week_program,
    classrooms,
    classrooms_lectures
):
    # print({
    #     day: get_lecture_day_valid_hours(lecture, week_program, day)
    #     for day in week_program
    # })

    positions = [
        (
            hours,
            day,
            sum(
                sum(map(
                    lambda x: x[lecture["id"]],
                    week_program[day][hour]["score"]
                )) + (1 / len(week_program[day][hour]["lectures_to_add"]))# + \
                # (1 / len(available_classrooms))
                
                for hour in hours.keys()
            ),
            get_shared_items_between_lists(
                *[
                    [
                        room_id
                        for room_id in week_program[day][hour]["available_classrooms"]
                        if room_id in classrooms_lectures[lecture["id"]]
                        if classrooms[room_id]["capacity"] >= len(lecture["studentIds"])
                    ]
                    for hour in hours
                ]
            )
        )
        for day in week_program
        for hours in get_lecture_day_valid_hours(lecture, week_program, day)
    ]

    return sorted(
        positions,
        key=lambda x: x[2],
        reverse=True
    )

def get_lecture_min_entropy_position(
    lecture,
    week_program,
    # classrooms,
    # classrooms_lectures
):
    best_hours = None
    best_day = None
    best_score = 0

    for day in week_program:
        hours_list = get_lecture_day_valid_hours(lecture, week_program, day)

        for hours in hours_list:
            score = 0
            for hour in hours:
                score += sum(map(
                    lambda x: x[lecture["id"]],
                    week_program[day][hour]["score"]
                )) + \
                    (1 / len(week_program[day][hour]["lectures_to_add"]))# + \
                    # (1 / len(available_classrooms))

            if score > best_score:
                best_score = score
                best_hours = hours
                best_day = day

    return best_hours, best_day, best_score
