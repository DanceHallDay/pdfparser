#include "pybind11/pybind11.h"
#include "pybind11/stl.h"
#include "poppler/cpp/poppler-document.h"
#include "poppler/cpp/poppler-page.h"


namespace py = pybind11;


struct text_data
{
    std::string text;
    double x;
    double y;
    double height;
    double width;
    int page;
};


std::string to_stdstring(poppler::ustring ust)
{
    std::vector<char> vc = ust.to_utf8();
    return std::string(vc.begin(), vc.end());
}


text_data textbox_to_textdata(poppler::text_box &tb, int page_nmbr)
{
    text_data td;
    td.text = to_stdstring(tb.text());
    td.x = tb.bbox().x();
    td.y = tb.bbox().y();
    td.height = tb.bbox().height();
    td.width = tb.bbox().width();
    td.page = page_nmbr;
    return td;
}


poppler::page* read_page(poppler::document *doc, int page_nmbr)
{
    return doc->create_page(page_nmbr);
}


int get_page_nmbr(poppler::document *doc)
{
    return doc->pages();
}


py::list get_text_data(std::string file_name)
{
    poppler::document *doc = poppler::document::load_from_file(file_name);
    std::vector<text_data> td;
    const int number_of_pages = doc->pages();
    for(int i=0; i<number_of_pages; i++)
    {
        poppler::page* page = read_page(doc, i);
        std::vector<poppler::text_box> tb = page->text_list();
        for(auto & j : tb)
        {
            td.push_back(textbox_to_textdata(j, i));
        }
        
    }
    py::list res = py::cast(td);
    return res;
}


PYBIND11_MODULE(pdf2text, m) {
    m.doc() = "pybind11 example plugin";
    py::class_<text_data>(m, "TextData")
   .def_readwrite("text", &text_data::text)
   .def_readwrite("x", &text_data::x)
   .def_readwrite("y", &text_data::y)
   .def_readwrite("height", &text_data::height)
   .def_readwrite("width", &text_data::width)
   .def_readwrite("page", &text_data::page);

    m.def("get_text_data", &get_text_data);

}
