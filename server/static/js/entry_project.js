jQuery(document).ready(function($) {
    var MONTHS = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ];
    var changes = [];

    function updateValue(key, value) {
        value = value || data[key];
        if ($.isArray(value)) {
            for (i=0; i<value.length; i++) {
                var newkey = key + '.' + i;
                var newvalue = value[i];
                updateValue(newkey, newvalue)
            }
        } else if ($.isPlainObject(value)) {
            for (subkey in value) {
                var newkey = key + '.' + subkey;
                var newvalue = value[subkey];
                updateValue(newkey, newvalue)
            }
        } else {
            if (key.substring(0,2) != '__') {
                var input = $('[name="'+key+'"]');
                input.val(value);
                input.closest('.form-group').removeClass('warning');
            } else if (key == '__project_url') {
                var link = $('a#__project_url');
                link.attr('href', value);
                link.removeAttr('disabled');
            }
        }
    }

    function updateDates(key, values) {
        var expenditure = $('#'+key+'-expenditure')
        var progress = $('#'+key+'-progress')
        var template;
        var block;
        var date;

        for (i=0; i<values.length; i++) {
            value = values[i];
            date = new Date(value['date']);

            block = $('#'+key+'-'+i+'-expenditure');
            if (block.length) {
                block.find('date-label').text(MONTHS[date.getMonth()]+' '+date.getFullYear());
                block.find('input').val(value['expenditure']).attr({
                    type: 'text',
                    id: key+'.'+i+'.expenditure',
                    name: key+'.'+i+'.expenditure'
                });
            } else {
                block = $('<div/>', {
                    addClass: 'date-block col-xs-1',
                    attr: { id: key+'-'+i+'-expenditure'}
                });
                block.append($('<div/>', {
                    addClass: 'date-label', 
                    text: MONTHS[date.getMonth()]+' '+date.getFullYear()
                }));
                block.append($('<input/>', {
                    val: value['expenditure'],
                    attr: {
                        type: 'text',
                        id: key+'.'+i+'.expenditure',
                        name: key+'.'+i+'.expenditure'
                    }
                }));
                $('#'+key+'-expenditure').append(block);
            }

            block = $('#'+key+'-'+i+'-progress');
            if (block.length) {
                block.find('date-label').text(MONTHS[date.getMonth()]+' '+date.getFullYear());
                block.find('input').val(value['progress']).attr({
                    type: 'text',
                    id: key+'.'+i+'.progress',
                    name: key+'.'+i+'.progress'
                });
            } else {
                block = $('<div/>', {
                    addClass: 'date-block col-xs-1',
                    attr: { id: key+'-'+i+'-progress'}
                });
                block.append($('<div/>', {
                    addClass: 'date-label', 
                    text: MONTHS[date.getMonth()]+' '+date.getFullYear()
                }));
                block.append($('<input/>', {
                    val: value['progress'],
                    attr: {
                        type: 'text',
                        id: key+'.'+i+'.progress',
                        name: key+'.'+i+'.progress'
                    }
                }));
                $('#'+key+'-progress').append(block);
            }
        }


        $('#'+key+'-expenditure').closest('.form-group').removeClass('warning');
        $('#'+key+'-progress').closest('.form-group').removeClass('warning');
    }

    function updateForm(d) {
        if (d) {
            data = d;
        }
        var values = data;
        for (key in values) {
            var value = d[key];
            if ((key == 'actual') || (key == 'planning')) {
                updateDates(key, value);
            } else {
                updateValue(key, value);
            }
        }
    }

    updateForm(data);

    $('input').on('change', function() {
        var element = $(this);
        var name = element.attr('name');
        var val = element.val();
        var data = { csrfmiddlewaretoken: csrf_token };

        element.closest('.form-group').addClass('warning');

        data[name] = val;
        for (i=0; i<changes.length; i++) {
            var c = changes[i];
            data[c['name']] = c['value'];
        }
        $.ajax({
            url: 'edit',
            method: 'POST',
            data: data
        }).success(function(data) {
            updateForm(data);
        }).error(function() {
            changes.push({ name: name, value: val });
        });
    })

    $('textarea').on('change', function() {
        var element = $(this);
        var name = element.attr('name');
        var val = element.val();
        var data = { csrfmiddlewaretoken: csrf_token };

        element.closest('.form-group').addClass('warning');

        data[name] = val;
        for (i=0; i<changes.length; i++) {
            var c = changes[i];
            data[c['name']] = c['value'];
        }
        $.ajax({
            url: 'edit',
            method: 'POST',
            data: data
        }).success(function(data) {
            updateForm(data);
        }).error(function() {
            changes.push({ name: name, value: val });
        });
    })

    $('select').on('change', function() {
        var element = $(this);
        var name = element.attr('name');
        var val = element.val();
        var data = { csrfmiddlewaretoken: csrf_token }

        element.closest('.form-group').addClass('warning');

        data[name] = val;
        for (i=0; i<changes.length; i++) {
            var c = changes[i];
            data[c['name']] = c['value'];
        }
        $.ajax({
            url: 'edit',
            method: 'POST',
            data: data
        }).success(function(data) {
            updateForm(data);
        }).error(function() {
            changes.push({ name: name, value: val });
        });
    });

    $('input[type="button"]').on('click', function() {
        var element = $(this);
        var name = element.attr('name');
        var val = element.val();
        var data = { csrfmiddlewaretoken: csrf_token };

        if (name == '__save') {
            var modal = $('#savingModal');
            modal.find('p').text('Your changes are being saved. Please wait.');
            modal.modal('show');
        }

        data[name] = val;
        for (i=0; i<changes.length; i++) {
            var c = changes[i];
            data[c['name']] = c['value'];
        }
        $.ajax({
            url: 'edit',
            method: 'POST',
            data: data
        }).success(function(data) {
            updateForm(data);
            var modal = $('#savingModal');
            modal.find('p').text('The project data has been succesfully saved.');
            setTimeout(function() {
                modal.modal('hide')
            }, 2000);
        }).error(function() {
            var modal = $('#savingModal');
            modal.find('p').text('Failed.');
            modal.modal('hide');
            alert('Your request has failed. Please try again.');
        });
    })

    $('#manager').typeahead({
        source: function( query, process ) {
            $.post(
                url_entry_coordinator,
                {
                    query: query
                },
                function(data) {
                    process(data);
                }
            );
        },
    });

    $('#contractor').typeahead({
        source: function( query, process ) {
            $.post(
                url_entry_contractor,
                {
                    query: query
                },
                function(data) {
                    process(data);
                }
            );
        },
    });

    $('.twitter-typeahead').css('display', 'block');

    function updatePlanningPhase() {
        var value = $(this).val()

        if (value == 'planning') {
            $('#planning_phase').closest('.form-group').css('display', '');
        } else {
            $('#planning_phase').closest('.form-group').css('display', 'none');
        }

        $('.hide-for-phase').css('display', '');
        $('.hide-for-'+value).css('display', 'none');
    };

    $('select[name="phase"]').on('change', updatePlanningPhase);
    updatePlanningPhase.call($('select[name="phase"]')[0]);

    function updateProgramme() {
        var data = { 'cluster': $(this).val() };
        $.ajax({
            url: url_entry_programme,
            method: 'GET',
            data: data
        }).success(function(data) {
            var programme = $('#programme');
            var selected = programme.val();
            programme.find('option').each(function() {
                var option = $(this);
                if (option.attr('value')) {
                    option.remove()
                }
            });
            $(data).each(function() {
                var option = $('<option/>');
                option.attr('value', this);
                option.text(this);
                if (this === selected) {
                    option.attr('selected', 'selected');
                }
                programme.append(option);
            });
            updateValue('programme');
        }).error(function() {
            alert('Unable to retrieve programmes for this cluster.');
        });
    };

    $('select[name="cluster"]').on('change', updateProgramme);
    updateProgramme.call($('select[name="cluster"]')[0]);

    $('.input-datepicker').datepicker({
        format: "yyyy-mm-dd",
        autoclose: true
    });
});
