def setup(app):
    from .extension import ExampleAdmonition
    app.add_directive("example", ExampleAdmonition)
    app.add_css_file("static/example_plate.css")
    return {"version": "0.1", "parallel_read_safe": True}