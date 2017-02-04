var gua_form = {};

gua_form.fromQuery = function (selector) {
    var tags = selector.find('[title]');
    var form = {};

    for (var tag of tags) {
        var key = tag.title;
        form[key] = tag.value;
    }

    return form;
};

gua_form.success = function (data) {
    console.log('succuss', data);
    location.reload();
};

gua_form.error = function (error) {
    console.log(error);
};

gua_form.send = function (url, form) {
    var data = JSON.stringify(form);
    console.log('send data', data);
    $.ajax({
        url: url,
        type: 'post',
        data: data,
        contentType: 'application/json',
        success: gua_form.success,
        error: gua_form.error
    });
};

gua_form.isValid = function (form) {
    // 16/12/01 限制发帖长度 2
    var minLength = 3;
    for (var key of Object.keys(form)) {
        var value = form[key];
        // todo 移除硬编码
        if (value.length < minLength && key != 'code' && !key.includes("id")) {
            alert('所有内容长度都必须大于 2');
            return false;
        }
    }
    return true;
};


gua_form.bindButtonEvent = function (url, form_jquery, button_jquery) {
    button_jquery.on('click', function () {
        var form = gua_form.fromQuery(form_jquery);
        var is_valid = gua_form.isValid(form);
        if (is_valid) {
            gua_form.send(url, form);
        }
    });
};


gua_form.toggle = function (form_jquery, button_jquery) {
    form_jquery.hide();
    var text_show = button_jquery.data('show');
    var text_hide = button_jquery.data('hide');
    button_jquery.text(text_show);

    button_jquery.click(function () {
        var display = form_jquery.css("display");
        if (display != "none") {
            form_jquery.slideUp();
            $(this).text(text_show);
        } else {
            form_jquery.slideDown();
            $(this).text(text_hide);
        }
    });
};

var initCodeMirror = function (code, language, target) {
    var options = {
        value: code,
        lineNumbers: true,
        readOnly: true,
        theme: 'material',
    };
    var mode, mime;
    var info = CodeMirror.findModeByName(language);
    if (info != undefined || info != null) {
        mode = info.mode;
        mime = info.mime;
    } else {
        info = CodeMirror.findModeByExtension(language);
        if (info != undefined || info != null) {
            mode = info.mode;
            mime = info.mime;
        } else {
            mode = 'python';
            mime = 'text/x-python';
        }
    }
    options['mode'] = mime;

    var editor = CodeMirror(target, options);
    editor.setSize("100%", "100%");
    CodeMirror.modeURL = "//cdn.bootcss.com/codemirror/5.18.2/mode/%N/%N.min.js";
    CodeMirror.autoLoadMode(editor, mode);
};

var renderMarkDown = function () {
    marked.setOptions({
        renderer: new marked.Renderer(),
        gfm: true,
        tables: true,
        breaks: true,
        pedantic: true,
    });

    $('.markdown-body').each(function () {
        var tag = $(this);
        var raw = tag.text();
        tag.html(marked(raw));
    });

    $('pre > code').each(function () {
        var tag = $(this);
        var target = this;

        var code = tag.text();
        tag.empty();

        var attr = tag.attr('class');
        var language;
        if (attr != undefined) {
            language = attr.split('-')[1];
        } else {
            language = 'python';
        }

        initCodeMirror(code, language, target)

    });
};