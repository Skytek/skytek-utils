import json_stream


def json_stream_to_builtin(data):
    if isinstance(
        data,
        (
            json_stream.base.PersistentStreamingJSONObject,
            json_stream.base.TransientStreamingJSONObject,
        ),
    ):
        return {k: json_stream_to_builtin(v) for k, v in data.items()}
    if isinstance(
        data,
        (
            json_stream.base.PersistentStreamingJSONList,
            json_stream.base.TransientStreamingJSONList,
        ),
    ):
        return [json_stream_to_builtin(v) for v in data]
    return data
