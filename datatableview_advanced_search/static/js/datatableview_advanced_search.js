// datatableview_advanced_search.js
require(['require', 'domReady'], function (require, domReady) {
    domReady(function () {
        require(['jquery', 'datatableview'], function ($, datatableview, datatables) {
            $(document).ready(function () {
                var search_inputs = $('.dataTables_filter input');
                button = '<span>&nbsp;&nbsp;&nbsp;<a class="advanced_search_help_lnk" data-target="#advanced_search_help" data-dismiss="modal"><i class="fa fa-question"></i></a></span>'
                search_inputs.each(function () {
                    var parent = $(this).parent();
                    $(button).appendTo(parent);
                });
                $(".advanced_search_help_lnk").on("click", function (e) {
                    console.log("click!!");
                    $('#advanced_search_help').modal('show');

                });

            });
        });
    });
});
