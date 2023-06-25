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


    /**
     * The function resizes the height of images in a carousel based on the height of a container element.
     */
    const resize_img_box = () => {
        let img_h = $("#wrapper .col-12").height() ;
        $("#hydrapp-carousel img").css('max-height', img_h) ;
    }


    /**
     * The function resizes the height of images in a carousel based on the height of a container element.
     */
    const resize_wrapper = () => {
        let nav_h = $("nav").height() ;
        $("#wrapper").css('height', "calc(100% - " + nav_h + "px)") ;
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


    /* This code is adding an event listener to the HTML input element with the ID "time". When the user
    presses the "Escape" key while the input element has focus, the `blur()` method is called on the
    input element, which removes focus from the element and hides the virtual keyboard on mobile
    devices. */
    $("#time").keyup(function(e) {
        if(e.key === "Escape") { 
            $(this).blur() ;
        }
    }) ;


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
    
        const data = {
            "csv":$("#data-type").val(),
            "run_reference":$("#run-reference").val(),
            "run-configuration":$("#run-configuration").val()
        } ;

        $.ajax({
			type: "POST",
			contentType: "application/json",
            data: JSON.stringify(data),
            url : "get-availables-date",
            success: function(result){
                if(result){
                    /** 
                     * This code is initializing a datepicker widget on an HTML input element with the ID "time". The
                     * `$.extend()` method is used to merge the default options for the datepicker with additional options
                     * specified in the object literal `{changeMonth: true, changeYear: true}`. The resulting options
                     * object is then passed as an argument to the `datepicker()` method to initialize the widget. The
                     * `$.datepicker.regional["it"]` object is used to set the regional settings for the datepicker to
                     * Italian. 
                     */
                    $("#time").datepicker( "destroy" ) ;

                    const options = $.extend(
                        {},
                        $.datepicker.regional["it"],{
                            changeMonth: true,
                            changeYear: true,
                            beforeShowDay: function(date){
                                var string = jQuery.datepicker.formatDate('yy-mm-dd', date);
                                if(result.indexOf(string) == -1){
                                    return [false, ""] ;
                                } else{
                                    return [true, ""] ;
                                }
                            }
                    }) ;
                    $("#time").datepicker(options) ;       
                } else{
                    window.location.href = "/" ;    
                }
            }
        })
    }


    /**
     * The function "get_images" sends a POST request to retrieve images based on user input and displays
     * them in a carousel format.
     * 
     * @param date The date parameter is a string representing a date in the format "YYYY-MM-DD". It is
     * used to specify the date for which images are requested.
     */
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
                $("#hydrapp-carousel-container").empty() ;
                if(result[0]){
                    if(result[1].length !== 0){
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

                        let html =    `<div id="hydrapp-carousel" class="carousel slide">
                                            <div class="carousel-inner">` + items + `</div>
                                            <button class="carousel-control-prev" type="button" data-bs-target="#hydrapp-carousel" data-bs-slide="prev">
                                                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                                <span class="visually-hidden">Previous</span>
                                            </button>
                                            <button class="carousel-control-next" type="button" data-bs-target="#hydrapp-carousel" data-bs-slide="next">
                                                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                                <span class="visually-hidden">Next</span>
                                            </button>
                                        </div>`

                        $("#hydrapp-carousel-container").append(html) ;
                        resize_img_box() ;
                        resize_wrapper() ;
                    }else{  
                        $("#hydrapp-carousel-container").append("<img class='img_placeholder' src='../static/img/placeholder.webp' alt='Immagine non trovata' />") ; 
                        resize_img_box() ;
                        resize_wrapper() ;
                    }
                }else{
                    window.location.href = "/" ; 
                }
            }
        })
    }

    const reset_selects = (x) => {
        $("#hydrapp-carousel-container").empty() ;
        
        switch(x) {
            case 1:
                $('#run-reference').prop('selectedIndex',0) ;
                $('#run-configuration').prop('selectedIndex',0) ;
                $('#time').datepicker('setDate', null) ;
                break ;
            case 2:
                $('#run-configuration').prop('selectedIndex',0) ;
                $('#time').datepicker('setDate', null) ;
                break ;
            case 3:
                $('#time').datepicker('setDate', null) ;
                break ;
          }
    }


	$("#data-type").on("change", function(){
		update_run_reference($(this).val(), $(this).attr("data-target"))
        reset_selects(1) ;
	}) ;

    $("#run-reference").on("change", function(){
		update_run_configuration($(this).val(), $(this).attr("data-target"))
        reset_selects(2) ;
	}) ;

    $("#run-configuration").on("change", function(){
        update_time()
        reset_selects(3) ;
    }) ;

    $("#time").on("change", function(){
        get_images($(this).val())
    }) ;

    resize_img_box() ;
    resize_wrapper() ;
    $(window).on('resize', function() {
        resize_img_box() ;
        resize_wrapper() ;
    }) ;

})(jQuery) ;