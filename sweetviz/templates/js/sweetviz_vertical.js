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
// hideAllDetails();

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
    $("#" + $(this).data("rollover-span")).addClass("bg-tab-summary-rollover-vertical");
    $("#" + $(this).data("rollover-span")).show();
    g_lastHovered = "#" + $(this).data("detail-div");
    },
// EXIT function
function(event) {
    // Rollover end!
    // hideAllDetails();
    //FBFB        $("#" + $(this).data("detail-div")).hide();
    }
);

// EVENT: SUMMARY CLICK
// $(".container-feature-summary, .container-feature-summary-target").click(function(event) {
$(".selector").click(function(event) {
    if ($(this).parent().parent().data('expanded') != 'true')
    {
        // EXPAND
        // --------------------------------------------------------
        $("#" + $(this).data("detail-div")).show();
        $(this).parent().parent().data('expanded', 'true');
        //alert($(this).parent().attr('id').substring(8) );

        var feature_index_str = $(this).parent().attr('id').substring(8);
        if ($(this).parent().attr('id') == "summary-target") {
            // Special feature name for target, so use common index notation for the following tasks
            feature_index_str = "f-1";
        }
        if ($('#cat-assoc-window-'+feature_index_str).length) {
            // CATEGORICAL feature: use variable-height window
            var $el = $('#detail_breakdown-' + feature_index_str);  //record the elem so you don't crawl the DOM everytime
            // HACK: BUG IN BROWSERS? DIVING BY SCALE HERE...
            var bottom = ($el.position().top / g_scale) + $el.outerHeight(true); // passing "true" will also include the top and bottom margin
            var desiredBottomBreakdown = bottom + 157;

            $el = $('#cat-assoc-window-' + feature_index_str);  //record the elem so you don't crawl the DOM everytime
            var bottomAssoc = $el.position().top + $el.outerHeight(true); // passing "true" will also include the top and bottom margin
            var desiredBottomAssoc = bottomAssoc + 166;

            var finalHeight = Math.max(desiredBottomBreakdown, desiredBottomAssoc);
            if ($(this).parent().attr('id') == "summary-target")
            {
                // More special processing for the target: change its background and limit its height (so it doesn't show through others below)
                // (Here, make the Height a bit taller so the black background shows through)
               $(this).parent().css('height', String((finalHeight + 50))+ 'px');
               $("#summary-target").css("overflow", "hidden");
            }
            $(this).parent().parent().css('height', String(finalHeight) + 'px');
        }
        else
        {
            // NON-CATEGORICAL feature: use fixed height window
            $(this).parent().parent().css('height', '1030px');
        }
        // Use the "big" background image for the target
        if ($(this).parent().attr('id') == "summary-target")
        {
            $("#summary-target-bg").addClass("bg-tab-summary-target-full");
            $("#summary-target-bg").removeClass("bg-tab-summary-target");
        }

        // HACK: For SOME reason, a selection gets made when we change what is hidden, unselect it
        let sel = document.getSelection();
        sel.removeAllRanges();

        // Animate to the top of the screen when expanding, so we can see the whole thing immediately
        $('html,body').animate(
            {scrollTop: $("#" + $(this).parent().attr('id')).offset().top}, 'fast');
    }
    else
    {
        // CONTRACT
        // --------------------------------------------------------
        $("#" + $(this).data("detail-div")).hide();

        // HACK: For SOME reason, a selection gets made when we change what is hidden, unselect it
        let sel = document.getSelection();
        sel.removeAllRanges();

        $(this).parent().parent().data('expanded', 'false');
        $(this).parent().parent().css('height', '161px');

        if ($(this).parent().attr('id') == "summary-target")
        {
            $("#summary-target-bg").removeClass("bg-tab-summary-target-full");
            $("#summary-target-bg").addClass("bg-tab-summary-target");
        }
    }
    // var offTop = $("#" + $(this).parent().attr('id')).offset().top;
  //  $('html,body').scrollTop(offTop);
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
// $("#button-summary-associations-source, #button-summary-associations-compare").hover(
//     // ENTER function
//     function()
//     {
//         if(g_snapped=="")
//         {
//             hideAllDetails();
//             $("#df-assoc").show();
//             //$("#df-assoc").show();
//         }
//         g_lastHovered = "#df-assoc";
//     },
//     // EXIT function
//     function()
//     {
//         if(g_snapped=="")
//         {
//             hideAllDetails();
//         }
//     });
// );

// ASSOCIATIONS CLICK
$("#button-summary-associations-source, #button-summary-associations-compare").click(function(event) {
    let actual_div = "#" + $(this).data("detail-div");
    // Quick hack: just remove the selected state to both buttons and restore if needed
    $("#button-summary-associations-source, #button-summary-associations-compare").removeClass("button-assoc-selected");
    $("#button-summary-associations-source, #button-summary-associations-compare").addClass("button-assoc");
    if(g_snapped == actual_div)
    {
        // DESELECT/HIDE ASSOC
        // --------------------------------------------------------
        g_snapped = "";
        $(actual_div).hide();
        $(".page-all-summaries").css({top: "160px"});
        // $(this).removeClass("button-assoc-selected");
        // $(this).addClass("button-assoc");
    }
    else if(g_snapped == "")
    {
        // SELECT/SHOW ASSOC
        // --------------------------------------------------------
        g_snapped =  actual_div;
        $(actual_div).show();
        $(".page-all-summaries").css({top: "993px"});
        $(this).addClass("button-assoc-selected");
    }
    else
    {
        // SWAP to OTHER ASSOC: DESELECT old, select new
        // --------------------------------------------------------
        $(g_snapped).hide();
        g_snapped =  actual_div;
        $(this).addClass("button-assoc-selected");
        $(actual_div).show();
    }
});


// DETAIL GRAPH BUTTONS
$(".button-bin").click(function() {
    which_id = $(this).attr('data-target');
    $("#"+which_id).attr('class', $(this).attr('data-new_class') + " pos-detail-num-graph");
});


}); // $(document).ready(...
