let g_snapped = "";
// let g_lastHovered = "";

function hideAllDetails()
{
    $(".container-feature-detail").hide();
    $(".container-df-associations").hide();
    $("span.bg-tab-summary-rollover").hide();
    $("#button-summary-associations-source, #button-summary-associations-compare").removeClass("button-assoc-selected");
    $("#button-summary-associations-source, #button-summary-associations-compare").addClass("button-assoc");
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
    if(g_snapped=="")
    {
        // Rollover start!
        $(".container-feature-detail").hide();
        $("span.bg-tab-summary-rollover").hide();
        $("#" + $(this).data("detail-div")).show();
        $("#" + $(this).data("rollover-span")).removeClass("bg-tab-summary-rollover-locked");
        $("#" + $(this).data("rollover-span")).addClass("bg-tab-summary-rollover");
        $("#" + $(this).data("rollover-span")).show();
    }
    // g_lastHovered = "#" + $(this).data("detail-div");
    },
// EXIT function
function(event) {
    if(g_snapped=="")
    {
        // Rollover end!
        hideAllDetails();
//FBFB        $("#" + $(this).data("detail-div")).hide();
    }
    }
);
// EVENT: SUMMARY CLICK
// $(".container-feature-summary, .container-feature-summary-target").click(function(event) {
$(".selector").click(function(event) {
    // No matter what, we should deselect the associations buttons
    $("#button-summary-associations-source, #button-summary-associations-compare").removeClass("button-assoc-selected");
    $("#button-summary-associations-source, #button-summary-associations-compare").addClass("button-assoc");

    // alert($(this).parent().attr('id'));
    let this_to_snap=$(this).parent().attr('id');

    if(g_snapped == this_to_snap)
    {
        // "Unselect"
        $("#" + $(this).data("rollover-span")).removeClass("bg-tab-summary-rollover-locked");
        $("#" + $(this).data("rollover-span")).addClass("bg-tab-summary-rollover");
        g_snapped = "";
    }
    else if (g_snapped == "")
    {
        // "Select"
        $("#" + $(this).data("rollover-span")).removeClass("bg-tab-summary-rollover");
        $("#" + $(this).data("rollover-span")).addClass("bg-tab-summary-rollover-locked");
        g_snapped = $(this).parent().attr('id');
        //$("#" + $(this).data("detail-div")).show();
        //$(g_lastHovered).show();
        // alert(this.parent().id);
    }
    else if (g_snapped !== this_to_snap) // implied
    {
        // "Select" while another was previously selected
        $("#" + $("#"+g_snapped).children().data("rollover-span")).removeClass("bg-tab-summary-rollover-locked");
        $("#" + $("#"+g_snapped).children().data("rollover-span")).addClass("bg-tab-summary-rollover");

        $(".container-feature-detail").hide();
        $("span.bg-tab-summary-rollover").hide();
        $("#" + $(this).data("detail-div")).show();
        
        $("#" + $(this).data("rollover-span")).removeClass("bg-tab-summary-rollover");
        $("#" + $(this).data("rollover-span")).addClass("bg-tab-summary-rollover-locked");
        $("#" + $(this).data("rollover-span")).css("display","inline");
        g_snapped = $(this).parent().attr('id');
    }
/*
    if (g_snapped != "")
    {
        $('html,body').animate(
            {scrollTop: $("#" + g_snapped).offset().top},
            'fast');

    }

 */
}
);
/*
$(window).scroll(function(e){
  var $el = $('.container-feature-detail');
    $el.css({'position': 'fixed', 'top': '0px'});

});
function fix_scroll() {
  var s = parseFloat($(window).scrollTop()) / 0.6;
  var fixedTitle = $('.container-feature-detail');
  fixedTitle.css('position','absolute');
  fixedTitle.css('top',s + 'px');
}fix_scroll();

$(window).on('scroll',fix_scroll);
*/

// ---------------------------------------------------------------------------------------------------------------------------
// SPECIFIC BUTTONS
// ---------------------------------------------------------------------------------------------------------------------------
// SUMMARY: ASSOCIATIONS -> HOVER
// --------------------------------------------------------
$("#button-summary-associations-source, #button-summary-associations-compare").hover(
    // ENTER function
    function()
    {
        if(g_snapped=="")
        {
            hideAllDetails();
            $("#" + $(this).data("detail-div")).show();
            // $("#df-assoc").show();
            //$("#df-assoc").show();
        }
        // g_lastHovered = "#df-assoc";
    },
    // EXIT function
    function()
    {
        if(g_snapped=="")
        {
            hideAllDetails();
        }
    });

// SUMMARY: ASSOCIATIONS -> CLICK
// --------------------------------------------------------
$("#button-summary-associations-source, #button-summary-associations-compare").click(function(event) {
    // Quick hack: just remove the selected state to both buttons and restore if needed
    $("#button-summary-associations-source, #button-summary-associations-compare").removeClass("button-assoc-selected");
    $("#button-summary-associations-source, #button-summary-associations-compare").addClass("button-assoc");
    let this_to_snap=this.id;
    if(g_snapped == this_to_snap)
    {
        // DESELECT/HIDE ASSOC
        // --------------------------------------------------------
        g_snapped = "";
    }
    else if(g_snapped=="")
    {
        // SELECT/SHOW ASSOC (Hide other one if already shown)
        // --------------------------------------------------------
        //$(".container-feature-detail").hide();
        //alert("#" + this.id+" GS:"+g_snapped);
        //$("#df-assoc").show();
        g_snapped = this.id;
        $(this).addClass("button-assoc-selected");
    }
    else
    {
        // SWAP to OTHER ASSOC: DESELECT old, select new
        // --------------------------------------------------------
        $("#" + $("#"+g_snapped).children().data("rollover-span")).removeClass("bg-tab-summary-rollover-locked");
        $("#" + $("#"+g_snapped).children().data("rollover-span")).addClass("bg-tab-summary-rollover");
        hideAllDetails();
        $(this).addClass("button-assoc-selected");
        g_snapped = this.id;
        $("#" + $(this).data("detail-div")).show();
    }
//    $(this).addClass("assoc_active");
});


// DETAIL GRAPH BUTTONS
$(".button-bin").click(function() {
    which_id = $(this).attr('data-target');
    $("#"+which_id).attr('class', $(this).attr('data-new_class') + " pos-detail-num-graph");
});


}); // $(document).ready(...
