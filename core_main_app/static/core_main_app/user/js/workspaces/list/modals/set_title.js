renameWorkspace = function() {
    $("#banner_set_title_errors").hide();
    var $recordRow = $(this).closest('tr');
    $('.'+functional_object+'-id').val($recordRow.attr("objectid"));
    $("#id_new_workspace_title").val($recordRow.find('td').first().text().trim());
    $("#rename-workspace-modal").modal("show");
};

rename_workspace = function(){
    var newTitle = $("#id_new_workspace_title").val().trim();
    if (newTitle === "") {
        $("#set_title_workspace_errors").html("Please provide a title.");
        $("#banner_set_title_errors").show(500);
        return;
    }

    $.ajax({
        url : setTitleWorkspaceUrl.replace("workspace_id", getSelectedDocument()),
        type : "PATCH",
        data: { title: newTitle },
		success: function(data){
			location.reload();
	    },
        error:function(data){
            var message = "A problem occurred while renaming the workspace.";
            try {
                message = JSON.parse(data.responseText).message || message;
            } catch (e) {}
            $("#set_title_workspace_errors").html(message);
            $("#banner_set_title_errors").show(500)
        }
    });
};


$('.rename-workspace-btn').on('click', renameWorkspace);
$('#rename-workspace-yes').on('click', rename_workspace);
