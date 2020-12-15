#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

template<class T> py::array Get1DArray(int len) {
	return py::array(py::buffer_info(
		nullptr,            /* Pointer to data (nullptr -> ask NumPy to allocate!) */
		sizeof(T),			/* Size of one item */
		py::format_descriptor<T>::format(), /* Buffer format */
		1,          /* How many dimensions? */
		{ len },  /* Number of elements for each dimension */
		{ sizeof(T) }  /* Strides for each dimension */
	));
}

int add(int x, int y){
	return x + y;
}

PYBIND11_MODULE(cppmodule, m) {

	m.doc() = R"pbdoc(
        pybind11 based python package
        -----------------------

        .. currentmodule:: cppmodule

        .. autosummary::
           :toctree: _generate

    )pbdoc";

	m.def("add", &add);
}
