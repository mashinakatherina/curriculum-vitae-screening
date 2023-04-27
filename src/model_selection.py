import os.path
import sys

from util.database import connect_database, get_deployment, get_metrics, add_deployment


def main():
    with open("../version.txt", "r") as version_file:
        version = int(version_file.readline()) + 1
    connection = connect_database()

    if get_deployment(connection, version) is not None:
        raise Exception("Deployment for version " + str(version) + " already exists")

    metrics = get_metrics(connection, version)
    if metrics is None:
        raise Exception("No metrics for version " + str(version) + " found")

    results = []
    for model in metrics:
        model_id = model[0]
        accuracy = model[1]
        duration = model[2]
        results.append((model_id, float(accuracy) * 10 - float(duration) / 10))
    results.sort(key=lambda x: x[1], reverse=True)
    best_result = results[0]

    prev_deployment = get_deployment(connection, version-1)
    if prev_deployment is not None and float(prev_deployment[1]) > best_result[1]:
        best_result = (int(prev_deployment[0]), float(prev_deployment[1]))
    add_deployment(connection, version, best_result)

    connection.close()


if __name__ == "__main__":
    main()
