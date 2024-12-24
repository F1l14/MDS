def scale_to_100(min_val, max_val, element):
    return (element - min_val) / (max_val - min_val) * 100