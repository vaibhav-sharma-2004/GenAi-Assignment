Prompt 1 — ETL Pipeline Optimization

Context:
I am building a batch ETL pipeline in Databricks using PySpark. The pipeline ingests transactional sales data from multiple CSV files stored in cloud storage and loads it into a Delta Lake table. The dataset size is approximately 500 GB daily, and the current job execution time exceeds 3 hours.

Role:
Act as a Senior Data Engineer with expertise in distributed data processing, PySpark optimization, and Delta Lake performance tuning.

Task:
Analyze the ETL logic and suggest optimizations to reduce execution time, improve scalability, and minimize resource consumption.

Constraints:

Focus only on performance optimization.
Assume the environment uses distributed compute clusters.
Avoid changing the business logic.
Suggestions should be production-grade and cost-efficient.
Include Spark-specific optimizations such as partitioning, caching, broadcast joins, and file compaction where applicable.

Format:
Provide the response in the following structure:

Performance Bottlenecks
Optimized Approach
Recommended Spark Configurations
Sample Optimized Code
Expected Performance Impact

Prompt 2 — Data Quality Validation Framework

Context:
I am designing a data quality validation framework for a healthcare analytics platform. Data is ingested from APIs, relational databases, and flat files into a centralized data lake. The system must validate schema consistency, null values, duplicate records, and referential integrity before loading curated tables.

Role:
Act as a Lead Data Quality Architect with expertise in data governance, validation frameworks, and enterprise-scale ETL systems.

Task:
Design a scalable and reusable data quality validation framework that can be integrated into modern ETL/ELT pipelines.

Constraints:

Use Python and SQL-based validation approaches.
The framework should support configurable validation rules.
Include logging, alerting, and audit tracking mechanisms.
Assume cloud-native architecture.
Avoid vendor-specific solutions unless necessary.

Format:
Provide:

High-Level Architecture
Validation Categories
Framework Components
Sample Validation Rules
Error Handling Strategy
Monitoring and Alerting Design

Prompt 3 — Data Pipeline Job Optimization

Context:
I am managing multiple large-scale ETL jobs running on a distributed data platform such as Databricks or Apache Spark. Some jobs are experiencing long execution times, high memory consumption, data skew issues, and cluster resource bottlenecks. The pipelines process billions of records daily from multiple data sources into a cloud data warehouse.

Role:
Act as a Senior Data Engineering Performance Optimization Expert with deep expertise in Spark, distributed computing, ETL orchestration, and workload tuning.

Task:
Analyze the ETL job execution logic and recommend optimizations to improve performance, reduce execution time, optimize resource utilization, and increase pipeline reliability.

Constraints:

Focus only on job and query performance optimization.
Assume a distributed compute environment.
Do not modify the underlying business logic.
Include recommendations related to partitioning, caching, broadcast joins, shuffle optimization, adaptive query execution, and cluster sizing.
Suggest monitoring and debugging techniques for identifying bottlenecks.
Recommendations should follow production best practices and be cost-efficient.

Format:
Provide the response in the following structure:

Identified Performance Issues
Root Cause Analysis
Recommended Optimizations
Spark/Cluster Configuration Improvements
Optimized Code Examples
Monitoring & Debugging Recommendations
Expected Performance Gains