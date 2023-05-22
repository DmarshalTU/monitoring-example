Total Number of Events Sent: This query will give you the total number of events sent by your application.
promql:
events_sent_total

Request Processing Time: This query will give you the average time spent processing requests:
rate(request_processing_seconds_sum[5m]) / rate(request_processing_seconds_count[5m])

This query uses the rate() function to calculate the per-second average rate of increase of the request_processing_seconds_sum and request_processing_seconds_count metrics over the last 5 minutes. Dividing the rate of the sum by the rate of the count gives the average request processing time.

CPU Usage: This query will give you the total CPU time spent by your application:
rate(process_cpu_seconds_total[5m])


Memory Usage: These queries will give you the virtual and resident memory size of your application:
process_virtual_memory_bytes
process_resident_memory_bytes

Python Garbage Collection: These queries will give you information about the Python garbage collectors activity:
rate(python_gc_objects_collected_total[5m])
rate(python_gc_objects_uncollectable_total[5m])
rate(python_gc_collections_total[5m])

Percentage of CPU Usage: This query will give you the percentage of CPU time spent by your application over a period of time:
100 * rate(process_cpu_seconds_total[5m])

This query multiplies the rate of CPU time spent by 100 to represent it as a percentage.
Rate of Events Sent: This query will give you the rate at which events are being sent by your application.:
rate(events_sent_total[5m])

Average Number of Objects Collected by Python's Garbage Collector: This query will give you the average number of objects collected by Python's garbage collector per collection:
rate(python_gc_objects_collected_total[5m]) / rate(python_gc_collections_total[5m])

Ratio of Uncollectable Objects: This query will give you the ratio of uncollectable objects found during garbage collection.:
rate(python_gc_objects_uncollectable_total[5m]) / rate(python_gc_objects_collected_total[5m])

Memory Usage Ratio: This query will give you the ratio of resident memory size to virtual memory size:
process_resident_memory_bytes / process_virtual_memory_bytes

Rate of File Descriptor Usage: This query will give you the rate at which your application is using file descriptors:
rate(process_open_fds[5m])