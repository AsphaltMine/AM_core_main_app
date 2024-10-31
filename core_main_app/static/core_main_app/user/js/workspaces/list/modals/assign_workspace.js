
/**
 * AJAX call
 */
load_form_change_workspace = function() {
    $("#assign-workspace-modal").modal("show");
    var $recordRow = $(this).parent().parent();

    // Get parent if btn in dropdown  (object id undefined)
    if (!$recordRow.attr("objectid")) $recordRow = $recordRow.parent()
    var documentId = $recordRow.attr("objectid") || "";
    $('.'+functional_object+'-id').val(documentId);

    $.ajax({
        url : changeWorkspaceUrl,
        type : "POST",
        dataType: "json",
        data : {
            // Only a single record has a workspace to preselect; bulk
            // selection intentionally leaves this blank.
            document_id: documentId,
            // `administration` was never actually declared anywhere (see
            // records_bulk_select.js) - `menu` (from init.raw.js) is the
            // real admin-vs-my-data flag.
            administration: (typeof menu !== 'undefined' && menu) ? 'True' : 'False'
        },
		success: function(data){
            $("#banner_assign_workspace_errors").hide();
            $("#assign-workspace-form").html(data.form);
	    },
        error:function(data){
            $("#form_assign_workspace_errors").html(data.responseText);
            $("#banner_assign_workspace_errors").show(500);
        }
    });
};

assign_workspace = function() {
    var workspace_id = $( "#id_workspaces" ).val().trim();

    // A bulk move on a large selection can take a while (chunked, one
    // request per 500 records) - close the modal right away and show the
    // same full-page "please wait" overlay used elsewhere, instead of
    // leaving the modal sitting open with no feedback.
    $("#assign-workspace-modal").modal("hide");
    if (typeof showLoading === 'function') {
        showLoading('Moving, please wait...');
    }

    // Each chunk reports its own assigned/skipped counts - aggregated
    // here so the user sees one final message instead of one per chunk.
    var totals = { assigned: 0, skipped: 0 };

    function doAssign(ids, onSuccess, onError) {
        $.ajax({
            url : assignWorkspaceUrl,
            type : "POST",
            dataType: "json",
            data : {
                workspace_id: workspace_id,
                document_id: ids
            },
            success: function(data){
                if (data) {
                    totals.assigned += data.assigned || 0;
                    totals.skipped += data.skipped || 0;
                }
                onSuccess();
            },
            error:function(data){
                if (typeof hideLoading === 'function') { hideLoading(); }
                $.notify(data.responseText || "A problem occurred while moving.", "danger");
                if (onError) onError();
            }
        });
    }

    function finish() {
        if (typeof hideLoading === 'function') { hideLoading(); }
        clearSelectionState();
        if (typeof queuePendingToast === 'function' && (totals.assigned || totals.skipped)) {
            var text = totals.assigned + ' item(s) moved.';
            if (totals.skipped) {
                text += ' ' + totals.skipped + ' could not be moved.';
            }
            queuePendingToast(text, totals.skipped ? 'warning' : 'success');
        }
        location.reload();
    }

    // If a whole chunk fails outright (rather than a partial, per-id
    // failure the backend already tolerates), stop instead of silently
    // hanging - the notification set in doAssign's error handler stays
    // visible, and whatever succeeded before the failing chunk is still
    // applied server-side.
    function stop() {
        if (typeof hideLoading === 'function') { hideLoading(); }
    }

    if (typeof resolveSelectedRecordIds === 'function') {
        resolveSelectedRecordIds(function(ids) {
            submitInChunks(ids, 500, doAssign, finish, stop);
        });
    } else {
        doAssign(getSelectedDocument(), finish, stop);
    }
};



$('.assign-workspace-record-btn').on('click', load_form_change_workspace);
$('#assign-workspace-yes').on('click', assign_workspace);