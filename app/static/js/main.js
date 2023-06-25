(function($) {
	"use strict" ;

	// Fill copyright footer & fix sidebar width
	$(document).ready(function(){
		const d = new Date() ;
		const year = d.getFullYear() ;
		const target = $('#copyright-txt') ;
		let msg ;
		msg = (year > "2023") ? "<span>Copyright © Fondazione CIMA 2023 - " + year + "</span>" : "<span>Copyright © Fondazione CIMA 2023</span>" ;	
		target.html(msg) ;	
	}) ;

    const options = $.extend(
        {},
        $.datepicker.regional["it"],
        {
            changeMonth: true,
            changeYear: true
        }) ;

    $("#time").datepicker(options) ;
    

    /**
     * The function resizes the height of images in a carousel based on the height of a container element.
     */
    const resize_img_box = () => {
        let img_h = $("#wrapper .col-12").height() ;
        $("#hydrapp-carousel img").css('max-height', img_h) ;
    }

	/**
     * The function updates a dropdown menu with options retrieved from a server using AJAX.
     * 
     * @param csv A string representing the CSV data to be sent in the AJAX request.
     * @param target The target parameter is a string that represents the ID of the HTML select element
     * that will be updated with new options after the AJAX call is successful.
     */
    const update_run_reference = (csv, target) => {
        const data = {
            "csv":csv,
            "target":target
        } ;

        $.ajax({
			type: "POST",
			contentType: "application/json",
            data: JSON.stringify(data),
            url : "update-run-reference",
            success: function(result){
                if(result){
                    const input =  $("#" + result[0]) ;
                    input.attr("disabled", false) ;
                    input.find('option').not(':first').remove() ;

                    $.each(result[1], function(key,value) {   
                        $("#" + result[0]).append($("<option></option>")
                        .attr("value", value[0])
                        .text(value[1])) ; 
                    }) ;
                } else {
                    window.location.href = "/" ; 
                }
            }
        })
    }
    
    /**
     * The function updates the run configuration using AJAX and populates options in a select element
     * based on the result.
     * 
     * @param run_reference A reference to a specific run configuration.
     * @param target The target parameter is a variable that represents the target of the run configuration
     * update. It is passed as a parameter to the update_run_configuration function.
     */
    const update_run_configuration = (run_reference, target) => {
        const data = {
            "csv":$("#data-type").val(),
            "run_reference":run_reference,
            "target":target
        } ;

        $.ajax({
			type: "POST",
			contentType: "application/json",
            data: JSON.stringify(data),
            url : "update-run-configuration",
            success: function(result){
                if(result){
                    const input =  $("#" + result[0]) ;
                    input.attr("disabled", false) ;
                    input.find('option').not(':first').remove() ;

                    $.each(result[1], function(key,value) {  
                        $("#" + result[0]).append($("<option></option>")
                        .attr("value", value[0])
                        .text(value[1])) ; 
                    }) ;
                } else {
                    window.location.href = "/" ; 
                }
            }
        })
    }

    /**
     * The function updates the run configuration using AJAX and populates options in a select element
     * based on the result.
     * 
     * @param run_reference A reference to a specific run configuration.
     * @param target The target parameter is a variable that represents the target of the run configuration
     * update. It is passed as a parameter to the update_run_configuration function.
     */
    const update_time = () => {
        $("#time").attr("disabled", false) ;
    }

    const get_images = (date) => {
        const data = {
            "date":date,
            "csv":$("#data-type").val(),
            "run_reference":$("#run-reference").val(),
            "run-configuration":$("#run-configuration").val()
        } ;

        $.ajax({
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(data),
            url : "get-images",
            success: function(result){
                if(result[0]){

                    let items = "" ;

                    $.each( result[1], function( key, value ) {
                        if( key == 0) {
                            items += `<div class="carousel-item active">
                                        <img src="` + value + `" class="d-block w-100" alt="...">
                                    </div>`   
                        } else {
                            items += `<div class="carousel-item">
                                        <img src="` + value + `" class="d-block w-100" alt="...">
                                    </div>`   
                        }
                    });

                    $("#hydrapp-carousel .carousel-inner").append(items) ;
                } else {
                    window.location.href = "/" ; 
                }
            }
        })
    }


	$("#data-type").on("change", function(){
		update_run_reference($(this).val(), $(this).attr("data-target"))
	}) ;

    $("#run-reference").on("change", function(){
		update_run_configuration($(this).val(), $(this).attr("data-target"))
	}) ;

    $("#run-configuration").on("change", function(){
		update_time()
	}) ;

    $("#time").on("change", function(){
		get_images($(this).val())
	}) ;


    resize_img_box() ;
    $(window).on('resize', function() {
        resize_img_box() ;
    }) ;

})(jQuery) ;