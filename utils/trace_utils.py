import datetime


def start_trace(context):
    context.tracing.start(screenshots=True, snapshots=True, sources=True)


def stop_trace(context, test_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    trace_path = f"reports/traces/{test_name}_{timestamp}.zip"
    context.tracing.stop(path=trace_path)

    return trace_path
