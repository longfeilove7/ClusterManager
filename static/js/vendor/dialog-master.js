"use strict";

var diaologMaster = function() {

    var universe = {};
    /**
    * @param id Id of div which should contain master form-note
    * @param masterTemplate array of objects which should contain form frames and fields
    */
    function init(id, masterTemplate, userCallback) {
        universe.parentNode = document.getElementById(id);
        universe.parentId = id;
        universe.masterTemplate = masterTemplate;
        universe.currentFrame = 0;
        universe.chainedFrame = null;
        universe.formaData = {};
        universe.callback = function(data) {
            return function () {
                if (validateFormData()) {
                    saveFrame();
                    userCallback(data);
                }
            }
        };

        universe.parentNode.style.overflow = "hidden";
        initFrame();
    }

    /**
    * Renders frame my template and current frameindex
    */
    function initFrame() {
        defineNextFrame();
        var fields = [];
        universe.masterTemplate[universe.currentFrame].map(function(fieldSettings) {
            // handle settings Object
            if (fieldSettings.type === "frameSettings") {
                universe.parentNode.style.height = !isNaN(fieldSettings.height) ? fieldSettings.height + "px" : "auto";
                return;
            }
            //handle form fields
            var innerNode;
            if (fieldSettings.type === "input" && fieldSettings.dataType !== "hidden") {
                innerNode = getInnerInput(fieldSettings);
            } else if (fieldSettings.type === "textarea") {
                innerNode = getInnerTextArea(fieldSettings);
            } else if (fieldSettings.type === "select") {
                innerNode = getInnerSelect(fieldSettings);
            } else if (fieldSettings.dataType === "hidden") {
                fields.push('<input id="' + fieldSettings.id + '" type="hidden" value="' + fieldSettings.defaultValue + '">');
                return;
            }
            fields.push(
                getFieldWrapper(innerNode, fieldSettings)
            );
        });
        fields.push(
            getFrameButton()
        );
        var validationAlertNode = '<div id="' + universe.parentId + '-validation-node" class="validation-node" style="height: 0px;"></div>';
        universe.parentNode.innerHTML = ['<form style="transition: all 0.5s; opacity: 1; left: 0; position: relative;">', validationAlertNode, fields.join(""), '</fields>'].join("");

        bindActionToButton();
    }
    /**
    * @return string containing input node
    */
    function getInnerInput(settings) {
        return '' +
            '<input class="form-control" ' +
                'type="' + settings.dataType + '" ' +
                'id="' + settings.id + '" '+
                (settings.style ? 'style="' + settings.style + '" ' : " ") +
                (settings.required ? 'required="" ' : " ") +
                (settings.defaultValue ? 'value="' + settings.defaultValue + '" ' : " ") +
                (settings.placeHolder ? 'placeHolder="' + settings.placeHolder + '" ' : " ") +
            '>';
    }
    /**
    * @return string containing text area node
    */
    function getInnerTextArea(settings) {
        return '' +
            '<textarea ' +
            'class="form-control" ' +
            'type="' + settings.dataType +'" ' +
            'id="' + settings.id + '" ' +
            (settings.style ? 'style="' + settings.style + '" ' : " ") +
            (settings.required ? 'required=""' : "") +
            'required="">' + (settings.defaultValue ? settings.defaultValue : "") + '</textarea>';

    }
    /**
    * @return string containing select node
    */
    function getInnerSelect(settings) {
        return '' +
            '<select id="' + settings.id + '" class="form-control form-control-sm">' +
                settings.options.map(function(option, index) {
                    return '<option value="' + option.value + '"' + (settings.selected === index ? " selected" : "") + '>' + option.title + '</option>';
                }).join("") +
            '</select>';
    }
    /**
    * @return string containing any wrapped input node
    */
    function getFieldWrapper(innerNode, fieldSettings) {
        return '' +
            '<div class="form-group row">' +
                '<label for="' + fieldSettings.id + '" class="col-md-2 col-12 col-form-label">' + fieldSettings.label + '</label>' +
                '<div class="col-md-10 col-12">' +
                    innerNode +
                '</div>' +
            '</div>';
    }
    /**
    * @return string containing button node for a frame
    */
    function getFrameButton() {
        if (universe.chainedFrame === "FINAL") {
            return '' +
                '<div class="form-group row">' +
                    '<div class="col-10 offset-md-2 offset-0">' +
                        '<a id="' + universe.parentId + '-process-button" class="btn btn-primary mx-0" href="javascript:void(0);">Send</a>' +
                    '</div>' +
                '</div>';
        }
        return '' +
            '<div class="form-group row">' +
                '<div class="col-10 offset-md-2 offset-0">' +
                    '<a id="' + universe.parentId + '-process-button" class="btn btn-primary mx-0" href="javascript:void(0);">Next</a>' +
                '</div>' +
            '</div>';
    }
    /**
    * Binds function to click listenner of button,
    * if it's the last frame we exec users callback with all forms params,
    * otherwise we store params and switch to the next frame
    */
    function bindActionToButton() {
        var onClickHandler;
        if (universe.chainedFrame === "FINAL") {
            onClickHandler = universe.callback(universe.formaData);
        } else {
            onClickHandler = switchToNextFrame;
        }
        document.getElementById("" + universe.parentId + "-process-button").addEventListener('click', onClickHandler);
    }
    /**
    * Switches to the next frame with animation
    */
    function switchToNextFrame() {
        if (!validateFormData()) {
            return;
        }
        saveFrame();
        var fromNode = universe.parentNode.getElementsByTagName("form")[0];
        fromNode.style.left = "1000px";
        fromNode.style.opacity = "0";
        setTimeout(function(){
            initFrame();
            fromNode = universe.parentNode.getElementsByTagName("form")[0];
            fromNode.style.left = "-1000px";
            fromNode.style.opacity = "0";
            setTimeout(function(){
                fromNode.style.left = "0";
                fromNode.style.opacity = "1";
            }, 100);
        }, 400);

    }
    /**
    * Defines which frame should be next
    */
    function defineNextFrame() {
        if (universe.currentFrame === 0 && universe.chainedFrame === null) {
            universe.masterTemplate[0].map(function(settings) {
                if (settings.type === "frameSettings") {
                    universe.chainedFrame = settings.chainedFrame;
                }
            });
            return;
        }
        universe.masterTemplate.map(function(frame, i) {
            frame.map(function(settings) {
                if (settings.type === "frameSettings" && universe.chainedFrame === settings.token) {
                    universe.currentFrame = i;
                    universe.chainedFrame = settings.chainedFrame;
                }
            });
        });
    }
    /**
    * Saves frame data
    */
    function saveFrame() {
        universe.masterTemplate[universe.currentFrame].map(function(fieldSettings, index) {
            var value;
            if (fieldSettings.type === "frameSettings") return;
            if (fieldSettings.type === "select") {
                value = document.getElementById(fieldSettings.id).options[document.getElementById(fieldSettings.id).selectedIndex].value;
                fieldSettings.options.map(function(option) {
                    if (option.value === value && option.chainedFrame) {
                        universe.chainedFrame = option.chainedFrame;
                    }
                })

            } else {
                value = document.getElementById(fieldSettings.id).value;
            }
            universe.formaData[fieldSettings.id] = value;
        });
    }
    function validateFormData() {
        var hasError = false;
        universe.masterTemplate[universe.currentFrame].map(function(fieldSettings) {
            if (fieldSettings.required && document.getElementById(fieldSettings.id).value.length === 0) {
                hasError = true;
                showNote("required");
            } else if (fieldSettings.dataType === "email" && !validateEmail(document.getElementById(fieldSettings.id).value)) {
                hasError = true;
                showNote("email");
            }
        });
        return !hasError;
    }
    function validateEmail(email) {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (!re.test(String(email).toLowerCase())) return false;
        return true;
    }
    function showNote(flag) {
        var noteNode = document.getElementById(universe.parentId + "-validation-node");
        if (!noteNode) return;

        noteNode.style.height = "50px";
        setTimeout(function() {
            noteNode.style.height = "0px";
        }, 3000);
        if (flag === "required") {
            noteNode.innerHTML = '<div class="alert alert-warning">' +
            'Please, fill out all required fields' +
            '</div>';
        } else if (flag === "email") {
            noteNode.innerHTML = '<div class="alert alert-warning">' +
            'Please, check your E-mail field' +
            '</div>';
        } else if (flag === "error") {
            noteNode.innerHTML = '<div class="alert alert-warning">' +
            'Error occured while sending, try later' +
            '</div>';
        }
    }
    function showError() {
        showNote("error");
    }
    function showSuccess() {
        var fromNode = universe.parentNode.getElementsByTagName("form")[0];
        fromNode.style.left = "1000px";
        fromNode.style.opacity = "0";
        setTimeout(function(){
            universe.parentNode.innerHTML = '<div class="alert alert-success" style="transition: all 0.5s; opacity: 1; left: 0; position: relative;">' +
            'Thank you! Your message has been successfully sent.' +
            '</div>';
            var noteNode = universe.parentNode.getElementsByClassName("alert-success")[0];
            noteNode.style.left = "-1000px";
            noteNode.style.opacity = "0";
            setTimeout(function(){
                noteNode.style.left = "0";
                noteNode.style.opacity = "1";
            }, 100);
        }, 400);
    }
    return {
        init: init,
        showError: showError,
        showSuccess: showSuccess
    };
}();
