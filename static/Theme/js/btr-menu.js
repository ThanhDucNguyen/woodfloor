/*!
* Bootstrap Responsive Menu (BTRmenu)
*  - v1.0 -
* Homepage: http://saigonpixel.vn/
* Author: ZhouHai
* Author Email: tuanhai.chau@gmail.com
*/

(function ($) {
    $.fn.btrmenu = function (options) {
        // START options
        var settings = $.extend({
            desktopsubmenuicon: true,
            mobileiconpack: "glyphicon",
            mobileopenicon: "glyphicon-chevron-down",
            mobilecloseicon: "glyphicon-chevron-up",
        }, options);
        // END options

        var thisul = this.find('ul').first();
        thisul.addClass("btr-menu");
        var responsive = false;
        if ($(window).width() < 768) {
            responsive = true;
        };
        //Submenu icon
        if (settings.desktopsubmenuicon && !responsive) {
            thisul.children('li').each(function () {
                var thiselement = $(this);
                if (thiselement.has('ul').length) {
                    thiselement.find('a').first().append(" <i class=\"caret\"></i>");
                };
                thiselement.find('li').each(function () {
                    var subelement = $(this);
                    if (subelement.has('ul').length) {
                        subelement.find('a').first().append(" <i class=\"caret\"></i>");
                    };
                });
            });
        }
        else if (responsive) {
            thisul.find('li').each(function () {
                var thiselement = $(this);
                if (thiselement.has('ul').length) {
                    thiselement.addClass('btr-dropdown');
                    thiselement.prepend("<span class='" + settings.mobileiconpack + " " + settings.mobileopenicon + " btrsubmenu-btn'></span>");
                }
            });

            $(".btr-menu .btrsubmenu-btn").click(function () {
                var element = $(this);
                var thisli = element.closest("li");
                var thisdropdown = element.closest("li").children("ul");
                var hasactive = false;
                if (!thisdropdown.hasClass("active")) {
                    hasactive = true;
                }
                // Clear all active
                thisli.closest('ul').find('ul').removeClass("active");
                if (hasactive) {
                    thisdropdown.addClass("active");
                };

                $(".btr-menu .btr-dropdown").each(function () {
                    var thisdropdownul = $(this).children('ul');
                    var thisdropdownbtn = $(this).children('.btrsubmenu-btn.' + settings.mobileiconpack);
                    if (thisdropdownul.hasClass("active") && thisdropdownbtn.hasClass(settings.mobileopenicon)) {
                        thisdropdownbtn.removeClass(settings.mobileopenicon).addClass(settings.mobilecloseicon);
                    }
                    else if (!thisdropdownul.hasClass("active") && thisdropdownbtn.hasClass(settings.mobilecloseicon)) {
                        thisdropdownbtn.removeClass(settings.mobilecloseicon).addClass(settings.mobileopenicon);
                    }
                });
            });
        }
    };
}(jQuery));