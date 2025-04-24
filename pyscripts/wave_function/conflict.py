from pyscripts.week_generator import get_shared_items_between_lists, get_sequence_subset, get_items_difference_sum
# from rich import print

def is_lectures_conflict(lecture1, lecture2):
    if lecture1["professor"]["id"] == lecture2["professor"]["id"]:
        return True

    if lecture1["year"] == lecture2["year"] and get_shared_items_between_lists(
            lecture1["studentIds"],
            lecture2["studentIds"]
        ):
        return True
    
    return False

def get_conflict_lectures_in_hour(week_program, day, hour, lecture):
    lec_ids = get_shared_items_between_lists(
        week_program[day][hour]["conflicts"][lecture["id"]],
        [
            lec["id"]
            for lec in week_program[day][hour]["lectures"]
        ]
    )
    
    return lec_ids

def get_lecture_day_valid_hours(lecture, week_program, day):
    hours = {}
    for hour in week_program[day]:
        if lecture["id"] not in week_program[day][hour]["lectures_to_add"]:
            continue

        l = get_conflict_lectures_in_hour(week_program, day, hour, lecture)

        hours[hour] = l
    
    # print("000000", lecture["id"], lecture["name"], lecture["hours"], day)
    # print(hours)

    hours_list = get_sequence_subset(list(hours.keys()), lecture["hours"])
    hours_list = [
        {
            h: hours[h]
            for h in hours_group
        }
        for hours_group in hours_list
        if get_items_difference_sum(hours_group) == len(hours_group) - 1
    ]

    # print(hours_list)

    return hours_list