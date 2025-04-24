from pyscripts.week_generator import get_items_distance_from_point

def generate_day_score_layer(week, day, hour, hours, match_func = lambda lec: False, m = 1):
    score_layer = {}
    for lec_id in week[day][hour]["conflicts"]:
        score_layer[lec_id] = 0
        
        if match_func(lec_id):
            score = m / (get_items_distance_from_point(hours, hour) + 1)
            score_layer[lec_id] = score
    
    return score_layer

def sum_score_layers(*score_layers):
    result = {}
    for score_layer in score_layers:
        for lec_id, score in score_layer.items():
            if lec_id in result:
                result[lec_id] += score
            else:
                result[lec_id] = score
    
    return result

def get_week_schedual_score(week_program):
    score = 0
    for day in week_program:
        for hour in week_program[day]:
            for i, lec in enumerate(week_program[day][hour]["lectures"]):
                score += week_program[day][hour]["score"][i][lec["id"]]
    return score