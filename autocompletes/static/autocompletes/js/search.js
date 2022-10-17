'use strict'

function search(obj) {
    if (obj.form.elements[obj.dataset.name]) {
        patch_url(obj.form.elements[obj.dataset.name], obj.name, obj.value)
    };
}

function patch_url(item, name, value) {
    django.jQuery.each(Object.keys(item), function(idx, key) {
        if (item[key].select2) {
            return patch_data(name, value, item[key].select2.dataAdapter.ajaxOptions, item[key].select2.dataAdapter.ajaxOptions.data)
        }
    })
}

function patch_data(name, value, ajaxOptions, baseData) {
   ajaxOptions.data = function (params) {
        let data = baseData(params)
        data[name] = value
        return data
   }
}
