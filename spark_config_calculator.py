# Spark Cluster Configuration Calculator
def calculate_spark_config(total_nodes, cores_per_node, ram_per_node, executor_cores,
                           parallelism_per_core=2, memory_overhead_percentage=10,
                           deployment_mode="Cluster"):
    print(f"Total Nodes: {total_nodes} (1 Master node + {total_nodes - 1} Worker nodes)")
    print(f"--executor-cores {executor_cores}")

    # System reservations
    yarn_cores = 1  # Yarn Daemon, 1 core per node

    # CALCULATED CLUSTER RESOURCES
    total_memory = total_nodes * ram_per_node
    total_overhead_memory = int(total_memory * (memory_overhead_percentage / 100))
    total_available_cores = (cores_per_node - yarn_cores) * total_nodes  # Leave 1 core per node for Hadoop/Yarn
    total_available_memory = total_memory - total_overhead_memory
    num_executors_per_node = int((cores_per_node - yarn_cores) / executor_cores)
    memory_per_executor = int((ram_per_node - 1) / num_executors_per_node)  # Leave 1 GB per node for Hadoop

    print("\n=====CALCULATED CLUSTER RESOURCES=====")
    print(f"Total memory (GB): {total_memory}")
    print(f"Total overhead memory (GB): {total_overhead_memory}")
    print(f"Total available cores: {total_available_cores}")
    print(f"Total available memory (GB): {total_available_memory}")
    print(f"Number of executors per node: {num_executors_per_node}")
    print(f"Memory per executor (GB): {memory_per_executor}")

    # Calculate total executors and default parallelism
    total_executors = (num_executors_per_node * total_nodes) - 1  # Leave 1 executor for ApplicationManager
    default_parallelism = total_executors * executor_cores * parallelism_per_core

    # Calculate memory values with overhead consideration
    memory_with_overhead = int(memory_per_executor * (1 - (memory_overhead_percentage / 100)))
    # Calculate memory overhead based on executor memory
    # The formula appears to be approximately: overhead = executor_memory_in_gb * 102.4 (rounded to nearest MB)
    memory_overhead = int(memory_with_overhead * 102.4)

    # SPARK-DEFAULTS.CONF
    spark_defaults = {
        'spark.default.parallelism': default_parallelism,
        'spark.executor.memory': memory_with_overhead,
        'spark.executor.instances': total_executors,
        'spark.driver.cores': executor_cores,
        'spark.executor.cores': executor_cores,
        'spark.driver.memory': memory_with_overhead,
        'spark.driver.maxResultSize': memory_with_overhead,
        'spark.driver.memoryOverhead': memory_overhead,
        'spark.executor.memoryOverhead': memory_overhead,
        'spark.dynamicAllocation.enabled': False,
        'spark.sql.adaptive.enabled': True
    }

    print("\n=====SPARK-DEFAULTS.CONF=====")
    for key, value in spark_defaults.items():
        print(f"{key}: {value}")

    return spark_defaults


def generate_spark_submit_command(spark_defaults):
    command = (
        "./bin/spark-submit "
        f"--name \"x app\" "
        "--class <app_class> "
        "--master yarn "
        "--deploy-mode cluster "
        f"--num-executors {spark_defaults['spark.executor.instances']} "
        f"--executor-memory {spark_defaults['spark.executor.memory']}g "
        f"--executor-cores {spark_defaults['spark.executor.cores']} "
        f"--driver-memory {spark_defaults['spark.driver.memory']}g "
        f"--driver-cores {spark_defaults['spark.driver.cores']} "
        f"--conf spark.default.parallelism={spark_defaults['spark.default.parallelism']} "
        f"--conf spark.driver.maxResultSize={spark_defaults['spark.driver.maxResultSize']}g "
        f"--conf spark.driver.memoryOverhead={spark_defaults['spark.driver.memoryOverhead']}m "
        f"--conf spark.executor.memoryOverhead={spark_defaults['spark.executor.memoryOverhead']}m "
        f"--conf spark.dynamicAllocation.enabled={str(spark_defaults['spark.dynamicAllocation.enabled']).lower()} "
        f"--conf spark.sql.adaptive.enabled={str(spark_defaults['spark.sql.adaptive.enabled']).lower()} "
    )
    return command


def main():
    print("\n=== Configuration 1 ===")
    config1 = calculate_spark_config(
        total_nodes=10,
        cores_per_node=16,
        ram_per_node=64,
        executor_cores=5
    )
    print("\nSpark Submit Command:")
    print(generate_spark_submit_command(config1))

    print("\n=== Configuration 2 ===")
    config2 = calculate_spark_config(
        total_nodes=5,
        cores_per_node=16,
        ram_per_node=32,
        executor_cores=5
    )
    print("\nSpark Submit Command:")
    print(generate_spark_submit_command(config2))

    print("\n=== Configuration 3 ===")
    config3 = calculate_spark_config(
        total_nodes=5,
        cores_per_node=16,
        ram_per_node=32,
        executor_cores=6
    )
    print("\nSpark Submit Command:")
    print(generate_spark_submit_command(config3))


if __name__ == "__main__":
    main()