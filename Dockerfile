FROM sphinxdoc/sphinx:8.1.3 AS build

WORKDIR /docs
COPY . /docs

RUN pip3 install --upgrade myst-parser \
    sphinxcontrib-redoc \
    sphinx-book-theme \
    # furo \
    # sphinx-press-theme \
    # piccolo-theme \
    # sphinxawesome-theme \
    # pydata-sphinx-theme \
    # sphinx-immaterial \
    sphinx-design \
    linkify-it-py \
    # sphinxcontrib-plantuml \
    sphinx-copybutton \
    # /docs/sphinx-tippy \
    # setuptools \
    sphinx-togglebutton \
    /docs/localextensions/sphinxcontrib-images \
    /docs/localextensions/example-plate \
    /docs/localextensions/translit-headers \
    /docs/localextensions/card-ext \
    /docs/localextensions/internal-docs

RUN make html

FROM nginx:1.27

EXPOSE 80

COPY --from=build /docs/build/html /usr/share/nginx/html