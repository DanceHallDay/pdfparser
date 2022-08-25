#include "pybind11/pybind11.h"
#include "pybind11/stl.h"
#include "poppler/cpp/poppler-document.h"
#include "poppler/cpp/poppler-page.h"


namespace py = pybind11;

struct text_data {
    std::string text;

    std::string fontname;
    double fontsize;

    double x;
    double y;
    double height;
    double width;

    int page;
};


class PDF {
    private: 
        poppler::document* doc;

    public: 
        PDF(std::string &filename) {
            doc = poppler::document::load_from_file(filename);
        }

        const int get_page_number() {
            return doc->pages();
        }

        py::list get_textdata() {
            std::vector<text_data> td;
            for(int i=0; i<get_page_number(); i++) {
                poppler::page* page = read_page(i);
                std::vector<poppler::text_box> tb = page->text_list();
                for(auto & j : tb) {
                    td.push_back(to_textdata(j, i));
                }
            }
            py::list res = py::cast(td);
            return res;
        }

    
    private:
        poppler::page* read_page(int page_number) {
            return doc->create_page(page_number);
        }

        std::string to_stdstring(poppler::ustring ust) {
            std::vector<char> vc = ust.to_utf8();
            return std::string(vc.begin(), vc.end());
        }

        text_data to_textdata(poppler::text_box &tb, int page_nmbr) {
            text_data td;
            td.text = to_stdstring(tb.text());
            td.fontsize = tb.get_font_size();
            td.fontname = tb.get_font_name();
            td.x = tb.bbox().x();
            td.y = tb.bbox().y();
            td.height = tb.bbox().height();
            td.width = tb.bbox().width();
            td.page = page_nmbr;
            return td;
        }
};


PYBIND11_MODULE(pdf2text, m) {
    py::class_<text_data>(m, "TextData")
        .def_readwrite("text", &text_data::text)
        .def_readwrite("fontname", &text_data::fontname)
        .def_readwrite("fontsize", &text_data::fontsize)
        .def_readwrite("x", &text_data::x)
        .def_readwrite("y", &text_data::y)
        .def_readwrite("height", &text_data::height)
        .def_readwrite("width", &text_data::width)
        .def_readwrite("page", &text_data::page);

    py::class_<PDF>(m, "PDF")
        .def(py::init<std::string &>())
        .def("get_page_number", &PDF::get_page_number)
        .def("get_text_data", &PDF::get_textdata);
}
