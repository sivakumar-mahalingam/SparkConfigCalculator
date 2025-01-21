# Spark Cluster Configuration Calculator

A Python utility for calculating optimal Apache Spark cluster configurations and generating corresponding spark-submit commands.

## Overview

This tool helps in calculating resource allocations and configurations for Apache Spark clusters. It takes into account various parameters such as number of nodes, cores per node, and RAM per node to generate optimized Spark configurations.

## Features

- Calculates cluster resource distributions
- Determines optimal executor configurations
- Generates spark-submit commands
- Handles memory overhead calculations
- Provides default parallelism settings

## Usage

### Basic Usage

```python
from spark_config_calculator import calculate_spark_config

config = calculate_spark_config(
    total_nodes=5,
    cores_per_node=16,
    ram_per_node=32,
    executor_cores=6
)
```

### Input Parameters

- `total_nodes`: Total number of nodes in the cluster
- `cores_per_node`: Number of cores per node
- `ram_per_node`: RAM per node in GB
- `executor_cores`: Number of cores per executor
- `parallelism_per_core`: Parallelism factor (default: 2)
- `memory_overhead_percentage`: Memory overhead percentage (default: 10)
- `deployment_mode`: Deployment mode (default: "Cluster")

### Output

The calculator provides:
1. Cluster resource calculations
2. Spark configuration parameters
3. Spark-submit command

## Resource Calculations

### Cluster Resources
- Total memory = nodes × RAM per node
- Total overhead memory = total memory × (overhead percentage / 100)
- Total available cores = (cores per node - yarn cores) × total nodes
- Available memory = total memory - overhead memory

### Executor Configurations
- Executors per node = (cores per node - yarn cores) / executor cores
- Memory per executor = (RAM per node - 1) / executors per node
- Total executors = (executors per node × total nodes) - 1

### Memory Overhead
Memory overhead is calculated using the formula:
```python
memory_overhead_mb = executor_memory_gb * 102.4
```
This formula allocates approximately 10% overhead (102.4 = 1024 * 0.1) of executor memory in MB.

## System Reservations

The calculator accounts for system overhead:
- 1 core per node reserved for YARN
- 1 GB memory per node reserved for Hadoop
- 1 executor reserved for Application Manager

## Example Configurations

### Large Cluster (10 nodes)
```python
config = calculate_spark_config(
    total_nodes=10,
    cores_per_node=16,
    ram_per_node=64,
    executor_cores=5
)
```

### Medium Cluster (5 nodes)
```python
config = calculate_spark_config(
    total_nodes=5,
    cores_per_node=16,
    ram_per_node=32,
    executor_cores=5
)
```

## Generated Configurations

The tool generates these key Spark configurations:
- spark.default.parallelism
- spark.executor.memory
- spark.executor.instances
- spark.executor.cores
- spark.driver.memory
- spark.driver.maxResultSize
- spark.driver.memoryOverhead
- spark.executor.memoryOverhead

## Notes

- Memory calculations include overhead for both driver and executor
- Default parallelism is calculated based on total executor cores and parallelism factor
- System resources are reserved for YARN and Hadoop operations
- Memory overhead is consistently calculated at approximately 10% of executor memory

## Best Practices

1. Adjust executor cores based on workload type:
   - CPU-intensive: Use more cores per executor
   - Memory-intensive: Use fewer cores per executor

2. Consider memory overhead when planning cluster resources

3. Monitor and adjust parallelism settings based on actual workload performance

## Dependencies

- Python 3.6 or higher

## License

This project is open source and available under the MIT License.
