import random
import copy
from models import *
from pyscripts.week_generator import *
from pyscripts.wave_function.conflict import *
from pyscripts.wave_function.entropy import *
from pyscripts.wave_function.score import *
# from rich import print

def place_lecture_in_week_schedual(lecture, week_program, day, hours, classroom, detailed_lectures):
    detailed_lectures[lecture["id"]]["hours"] -= lecture["hours"]

    for hour in hours:
        p = week_program[day][hour]

        lecture["classroom"] = copy.deepcopy(classroom)
        p["lectures"].append(lecture)
        
        p["lectures_to_add"].remove(lecture["id"])

        if classroom["id"] in p["available_classrooms"]: #### TODO remove
            p["available_classrooms"].remove(lecture["classroom"]["id"])

    for hour in week_program[day]:
        score_layer = sum_score_layers(
            generate_day_score_layer(
                week_program,
                day,
                hour,
                hours,
                lambda lec_id: detailed_lectures[lec_id]["professor"]["id"] == lecture["professor"]["id"],
                1,
            ),
            generate_day_score_layer(
                week_program,
                day,
                hour,
                hours,
                lambda lec_id: detailed_lectures[lec_id]["year"] == lecture["year"]
            )
        )
        week_program[day][hour]["score"].append(score_layer)
    
    return week_program, detailed_lectures

def place_lecture(
    lecture,
    week_program,
    detailed_lectures,
    classrooms,
    classrooms_lectures,
    const_ids = [],
):
    if not classrooms_lectures.get(lecture["id"]):
        return False, False

    items = get_lecture_sorted_entropy_positions(lecture, week_program, classrooms, classrooms_lectures)

    if not items:
        return False, False

    for hours, day, score, rooms in items:
        if sum(map(lambda x: len(x), hours.values())) == 0 and len(rooms):
            rooms = sorted(rooms, key=lambda x: classrooms[x]["capacity"])

            week_program, detailed_lectures = place_lecture_in_week_schedual(
                lecture,
                copy.deepcopy(week_program),
                day,
                list(hours.keys()),
                classrooms[rooms[0]],
                copy.deepcopy(detailed_lectures)
            )
            break
    else:
        for item in items:
            if not len(item[3]):
                continue
            
            rooms = sorted(item[3], key=lambda x: classrooms[x]["capacity"])

            lec_ids = list(set([
                id_
                for ids in item[0].values()
                for id_ in ids
            ]))
            for lec_id in lec_ids:
                if (detailed_lectures[lec_id]["professor"]["id"] == lecture["professor"]["id"] and detailed_lectures[lec_id]["hours"] > lecture["hours"]) \
                    or lec_id == lecture["id"] or lec_id in const_ids or len(get_shared_items_between_lists([
                            lec["id"]
                            for hour in item[0].keys()
                            for lec in week_program[item[1]][hour]["lectures"]
                            if lec.get("locked") # if "locked" in lec and "locked" is true
                        ],
                        lec_ids
                    )):
                    break
            else:
                ####################### TODO
                if len(item[3]):
                    rooms = sorted(item[3], key=lambda x: classrooms[x]["capacity"])
                else:
                    rooms = [classrooms[random.choice(classrooms_lectures[lecture["id"]])]["id"]]
                    print(lecture["name"], classrooms[rooms[0]], "hours", item[0], "day", item[1])
                    print("removed", list(set(lec_ids + [
                        id_
                        # week_program[item[1]][hour]["classrooms"][week_program[item[1]][hour]["lectures"].index(id_)]
                        for hour, ids in item[0].items()
                        for id_ in ids
                        if (week_program[item[1]][hour]["classrooms"][week_program[item[1]][hour]["lectures"].index(id_)]["id"]) == rooms[0]
                    ])))
                    lec_ids = list(set(lec_ids + [
                        id_
                        # week_program[item[1]][hour]["classrooms"][week_program[item[1]][hour]["lectures"].index(id_)]
                        for hour, ids in item[0].items()
                        for id_ in ids
                        if (week_program[item[1]][hour]["classrooms"][week_program[item[1]][hour]["lectures"].index(id_)]["id"]) == rooms[0]
                    ]))
                #######################
    
                w_p = copy.deepcopy(week_program)
                d_l = copy.deepcopy(detailed_lectures)

                for hour in item[0]:
                    for lec_id in item[0][hour]:

                        index = None
                        for index, lec in enumerate(w_p[item[1]][hour]["lectures"]):
                            if lec["id"] == lec_id:
                                break
                        else:
                            continue

                        lec = w_p[item[1]][hour]["lectures"][index]

                        d_l = remove_lecture_from_position(w_p, item[1], hour, lec, d_l)
                
                w_p, d_l = place_lecture_in_week_schedual(
                    lecture,
                    w_p,
                    item[1],
                    list(item[0].keys()),
                    classrooms[rooms[0]],
                    # classrooms[1],
                    d_l,
                )

                for lec_id in lec_ids:
                    w_p, d_l = place_lecture(
                        d_l[lec_id],
                        copy.deepcopy(w_p),
                        copy.deepcopy(d_l),
                        classrooms,
                        classrooms_lectures,
                        const_ids + [lecture["id"]],
                    )
                    if w_p is False:
                        break
                    else:
                        week_program = w_p
                        detailed_lectures = d_l
                else:
                    break
        else:
            return False, False
    
    return copy.deepcopy(week_program), copy.deepcopy(detailed_lectures)

def place_lecture_parts(lecture, week_program, detailed_lectures, classrooms, classrooms_lectures):
    lecs = [
        copy.deepcopy(lecture)
    ]

    while len(lecs):
        w_p, d_l = place_lecture(lecs[0], copy.deepcopy(week_program), copy.deepcopy(detailed_lectures), classrooms, classrooms_lectures)

        if w_p is False:
            if lecs[0]["hours"] <= 1:
                print(lecture["id"], lecture["name"], lecs[0]["hours"])
                return False, False

            h = lecs[0]["hours"]
            lecs[0]["hours"] = h - (h // 2)

            lec2 = copy.deepcopy(lecs[0])
            lec2["hours"] = h // 2

            lecs.append(
                lec2
            )
        else:
            week_program = w_p
            detailed_lectures = d_l
            lecs.pop(0)
    
    return week_program, detailed_lectures

def place_less_entropy_lecture(week_program, detailed_lectures, classrooms, classrooms_lectures):
    lectures_ids = [
        lec["id"]
        for lec in detailed_lectures.values()
        if lec["hours"] != 0
    ]

    # entropys = {
    #     lec_id: get_lecture_min_entropy_position(detailed_lectures[lec_id], week_program)[2]
    #     for lec_id in lectures_ids
    # }
    # min_entropy_lec_id = min(entropys, key=entropys.get)

    weights = [
        - (get_lecture_min_entropy_position(detailed_lectures[lec_id], week_program)[2] ** 2)
        for lec_id in lectures_ids
    ]
    if sum(weights) == 0:
        weights = [
            1
            for _ in weights
        ]
    else:
        min_weight = min(weights)
        weights = [
            weight - (min_weight * 2)
            for weight in weights
        ]
    min_entropy_lec_id = random.choices(lectures_ids, weights=weights, k=1)[0]

    lec = detailed_lectures[min_entropy_lec_id]

    # week_program = place_lecture(copy.deepcopy(lec), copy.deepcopy(week_program), detailed_lectures, classrooms, classrooms_lectures)
    week_program, detailed_lectures = place_lecture_parts(copy.deepcopy(lec), copy.deepcopy(week_program), copy.deepcopy(detailed_lectures), classrooms, classrooms_lectures)

    return week_program, detailed_lectures

def remove_lecture_from_hour(week_program, day, hour, lecture):
    week_program[day][hour]["lectures_to_add"].append(lecture["id"])
    week_program[day][hour]["available_classrooms"].append(lecture["classroom"]["id"])

    index = None
    for index, lec in enumerate(week_program[day][hour]["lectures"]):
        if lec["id"] == lecture["id"]:
            break
    
    week_program[day][hour]["lectures"].pop(index)
    week_program[day][hour]["score"].pop(index)

def remove_lecture_from_position(week_program, day, hour, lecture, detailed_lectures):
    detailed_lectures[lecture["id"]]["hours"] += lecture["hours"]

    h = hour
    while True:
        if h not in week_program[day]:
            break

        if lecture["id"] in [
            lec["id"]
            for lec in week_program[day][h]["lectures"]
        ]:
            remove_lecture_from_hour(week_program, day, h, lecture)

        h -= 1
    
    h = hour+1
    while True:
        if h not in week_program[day]:
            break

        if lecture["id"] in [
            lec["id"]
            for lec in week_program[day][h]["lectures"]
        ]:
            remove_lecture_from_hour(week_program, day, h, lecture)

        h += 1

    return detailed_lectures

# def remove_lecture_from_week(week_program, detailed_lectures, lecture):
#     for day in week_program:
#         for hour in week_program[day]:
#             if lecture["id"] in [
#                 lec["id"]
#                 for lec in week_program[day][hour]["lectures"]
#             ]:
#                 detailed_lectures = remove_lecture_from_position(week_program, day, hour, lecture, detailed_lectures)
    
#     return week_program, detailed_lectures

def get_genetic_week(week_program):
    for day in week_program:
        for hour in week_program[day]:
            week_program[day][hour] = week_program[day][hour]["lectures"]

def generate_week_schedual(week_program = None, detailed_lectures = None):
    if detailed_lectures is None:
        detailed_lectures = get_detailed_lectures()
    
    if week_program is None:
        week_program = generate_empty_week()

    classrooms = get_classrooms()
    classrooms_lectures = get_classrooms_lectures()
    
    detailed_lectures.sort(key=lambda x: x["year"])
    detailed_lectures.sort(key=lambda x: x["hours"], reverse=True)
    detailed_lectures.sort(key=lambda x: x["professor"]["id"])

    detailed_lectures = {
        lec["id"]: lec
        for lec in detailed_lectures
    }

    for day in week_program:
        for hour in week_program[day]:
            week_program[day][hour] = {
                "lectures_to_add": [],
                "conflicts": {},
                "score": [{}],
                "lectures": copy.deepcopy(week_program[day][hour]),
                "available_classrooms": list(
                    set(classrooms.keys()) ^ set([
                        lec["classroom"]["id"]
                        for lec in week_program[day][hour]
                    ])
                ),
            }

    for lec in detailed_lectures.values():
        for day in lec["professor"]["freeTime"]:
            for hour in lec["professor"]["freeTime"][day]:
                initial_score = 1 / (get_items_distance_from_point([hour], 12) + 1)
                week_program[day][hour]["score"][-1][lec["id"]] = initial_score
                week_program[day][hour]["lectures_to_add"].append(lec["id"])
                week_program[day][hour]["conflicts"][lec["id"]] = []

    for day in week_program:
        for hour in week_program[day]:
            for lec1_id in week_program[day][hour]["lectures_to_add"]:
                for lec2_id in week_program[day][hour]["lectures_to_add"]:
                    if lec1_id == lec2_id:
                        continue

                    if is_lectures_conflict(detailed_lectures[lec1_id], detailed_lectures[lec2_id]):
                        week_program[day][hour]["conflicts"][lec1_id].append(lec2_id)

    while sum([lec["hours"] for lec in detailed_lectures.values()]) > 0:
        w_p, d_l = place_less_entropy_lecture(copy.deepcopy(week_program), copy.deepcopy(detailed_lectures), classrooms, classrooms_lectures)
        if w_p is False:
            print("Failed to place lecture")
            print("Left lectures", sum([lec["hours"] > 0 for lec in detailed_lectures.values()]))
            # break
            return {
                "week_program": None,
                "score": None
            }
        week_program = w_p
        detailed_lectures = d_l
    
    # for lec in detailed_lectures.values():
    #     week_program, detailed_lectures = remove_lecture_from_week(copy.deepcopy(week_program), copy.deepcopy(detailed_lectures), copy.deepcopy(lec))
    #     week_program, detailed_lectures = place_lecture_parts(copy.deepcopy(lec), copy.deepcopy(week_program), copy.deepcopy(detailed_lectures), classrooms, classrooms_lectures)


    week_score = get_week_schedual_score(week_program)

    get_genetic_week(week_program)
    week_program = get_fully_detailed_week_program(week_program)

    return {
        "week_program": week_program,
        "score": week_score,
    }

# def generate_multiple_week_schedual_get_best(week_program, detailed_lectures, num=10):
#     week_scheduals = [
#         generate_week_schedual(copy.deepcopy(week_program), detailed_lectures)
#         for _ in range(num)
#     ]

#     best_week_schedual = max(week_scheduals, key=lambda x: x["score"])
#     return best_week_schedual