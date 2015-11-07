;
var UMy = (function ($, window, document, umy) {

    var API = function (){};

    API.prototype.getElementPosition = function (element){
        return $(element).offset();
    };

    API.prototype.loadPageToContainer = function(pageName, containerId){
        umy.containers = umy.containers || {};
        if(umy.containers[pageName] && umy.containers[pageName] != null) {
            $.getScript(pageName + "-clear.js", function() {
                eval("clear_" + pageName + "()");
            });
            umy.containers[pageName].empty();
        }
        umy.containers[pageName] = $("#" + containerId).attr("page", pageName);
        umy.containers[pageName].load(pageName + ".html", function() {
            $.getScript(pageName + ".js", function() {
                eval("init_" + pageName + "()");
            });
        });
	};

    API.prototype.loadPageToDialog = function (pageName, options, title) {
        var dialog = $("<div></div>").attr("title", (title || pageName));
        var dialogInner = $("<div class='ui-widget'></div>");
        options = options || {};
        options.autoOpen = false;
        var resultDialog = dialog.dialog(options);
        dialogInner.load(pageName + ".html", function () {
            $.getScript(pageName + ".js", function () {
                eval("init_" + pageName + "()");
            });
        });
        dialog.on("dialogclose.umy", (function (el) {
            return function (event, ui) {
                el.dialog("destroy");
                el.remove();
            };
        })(dialog));
        dialogInner.appendTo(dialog);
        dialog.dialog("open");
        dialog.dialog("moveToTop");
        return resultDialog;
    };

	
    umy.API = new API();

    return umy;

})(jQuery, window, document, UMy || {});