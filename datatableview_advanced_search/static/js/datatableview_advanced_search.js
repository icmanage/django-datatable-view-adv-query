// datatableview_advanced_search.js
require(['require', 'domReady'], function (require, domReady) {
    domReady(function () {
        require(['jquery', 'datatableview'], function ($, datatableview) {
            $(document).ready(function () {
                var search_inputs = $('.dataTables_filter input');
                button = '<span>&nbsp;&nbsp;&nbsp;<a class="advanced_search_help_lnk" data-target="#advanced_search_help" data-dismiss="modal"><i class="fa fa-question"></i></a></span>'
                search_inputs.each(function () {
                    $(button).appendTo($(this).parent());
                });
                $(".advanced_search_help_lnk").on("click", function (e) {
                    $('#advanced_search_help').modal('show');
                });

            });
        });
    });
});