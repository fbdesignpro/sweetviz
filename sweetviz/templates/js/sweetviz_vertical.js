let g_snapped = "";
let g_lastHovered = "";

function hideAllDetails()
{
    $(".container-feature-detail").hide();
    $(".container-df-associations").hide();
    $("span.bg-tab-summary-rollover").hide();
}


// GLOBAL EVENTS
// ---------------------------------------------------------------------------------------------------------------------------
// EVENT: [ANYWHERE] RIGHT-CLICK REMOVES SELECTION
// $(document).contextmenu(function() {
//     if (g_snapped != "")
//     {
//         g_snapped = "";
//         hideAllDetails();
//     }
//     if (g_lastHovered != "")
//     {
//         $(g_lastHovered).show();
//         //alert("#"+g_lastHovered);
//     }
//     return false;
// });

$("span.bg-tab-summary-rollover").hide();
hideAllDetails();

$(document).ready(function() {
// INITIALIZATION
// --------------------------------------------------------
hideAllDetails();
$("span.bg-tab-summary-rollover").hide();

// Make the detail column the same height, so the floating element has room
//$("#col2").height($("#col1").height());
$("#col1").height(g_height);
$("#col2").height(g_height);
//alert($("#col1").height());

// SUMMARY AREA
// --------------------------------------------------------
// EVENT: SUMMARY ROLLOVER
// $(".selector, .container-feature-summary-target").hover(
$(".selector").hover(
// ENTER function
function(event) {
    // Rollover start!
    // $(".container-feature-detail").hide();
    $("span.bg-tab-summary-rollover").hide();
    $("#" + $(this).data("rollover-span")).removeClass("bg-tab-summary-rollover-locked");
    $("#" + $(this).data("rollover-span")).addClass("bg-tab-summary-rollover");
    $("#" + $(this).data("rollover-span")).show();
    g_lastHovered = "#" + $(this).data("detail-div");
    },
// EXIT function
function(event) {
    // Rollover end!
    hideAllDetails();
    //FBFB        $("#" + $(this).data("detail-div")).hide();
    }
);

// EVENT: SUMMARY CLICK
// $(".container-feature-summary, .container-feature-summary-target").click(function(event) {
$(".selector").click(function(event) {
    if ($(this).parent().parent().data('expanded') != 'true')
    {
        $("#" + $(this).data("detail-div")).show();
        $(this).parent().parent().data('expanded', 'true');
        $(this).parent().parent().css('height', '1061px');
    }
    else
    {
        $("#" + $(this).data("detail-div")).hide();
        $(this).parent().parent().data('expanded', 'false');
        $(this).parent().parent().css('height', '161px');
    }
    // let thisIndex = $(this).parent().parent().data('order-index');
    //alert(thisIndex);
    // for (let i = parseInt(thisIndex) + 1; i < 10; i++) {
    //     let currentTop = $("#summary-pos-f" + i).attr('style')
    //     $("#summary-pos-f" + i).attr('style',
    // }
// if(g_snapped == $(this).parent().attr('id'))
//     {
//         $("#" + $(this).data("rollover-span")).removeClass("bg-tab-summary-rollover-locked");
//         $("#" + $(this).data("rollover-span")).addClass("bg-tab-summary-rollover");
//         g_snapped = "";
//     }
//     else if (g_snapped == "")
//     {
//         $("#" + $(this).data("rollover-span")).removeClass("bg-tab-summary-rollover");
//         $("#" + $(this).data("rollover-span")).addClass("bg-tab-summary-rollover-locked");
//         g_snapped = $(this).parent().attr('id');
// //        $("#" + $(this).data("detail-div")).show();
//         //$(g_lastHovered).show();
//         // alert(this.parent().id);
//     }
    }
);


// SPECIFIC BUTTONS
// ---------------------------------------------------------------------------------------------------------------------------
// SUMMARY: ASSOCIATIONS
$("#button-summary-associations").hover(
    // ENTER function
    function()
    {
        if(g_snapped=="")
        {
            hideAllDetails();
            $("#df-assoc").show();
            //$("#df-assoc").show();
        }
        g_lastHovered = "#df-assoc";
    },
    // EXIT function
    function()
    {
        if(g_snapped=="")
        {
            hideAllDetails();
        }
    });
// ASSOCIATIONS CLICK
$("#button-summary-associations").click(function(event) {
    if(g_snapped == this.id)
    {
        g_snapped = "";
    }
    else
    {
        //$(".container-feature-detail").hide();
        //alert("#" + this.id+" GS:"+g_snapped);
        //$("#df-assoc").show();
        g_snapped = this.id;
    }
});


// DETAIL GRAPH BUTTONS
$(".button-bin").click(function() {
    which_id = $(this).attr('data-target');
    $("#"+which_id).attr('class', $(this).attr('data-new_class') + " pos-detail-num-graph");
});


}); // $(document).ready(...
