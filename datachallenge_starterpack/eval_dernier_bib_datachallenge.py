def get_score(data: dict):
    """get top 1-2-3 scores of data prediction. Need to fix Y in function to compare input data to a Y golden standar.

    Args:
        data (dict): data dictionnary with prediction

    Returns:
        list: score list [top1, top2, top3] -> number of y in top1 - 2 - 3
    """
    
    top1 = 0
    top3 = 0
    top5 = 0

    Y = { # reference data to compare with
        "1": '5',
        "2": '3',
        "3": '1',
        "4": '7',
    }

    i = 0
    for k,v in data.items():
        if k not in Y:
            if k != "equipe":
                print(f"Attention : la requête {k} n'est pas dans le jeu de données à soumettre")
            continue
        i += 1
        rang = v.index(Y.get(k)) if Y.get(k) in v else 5
        if rang == 0:
            top1 += 1
            top3 += 1
            top5 += 1
        elif rang <= 2:
            top3 += 1
            top5 += 1
        elif rang <= 4:
            top5 += 1
            
    return [top1, top3, top5]


