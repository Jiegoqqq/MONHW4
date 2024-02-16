$(document).ready(function(){
    $.ajax({ 
        type: 'POST',
        url: '/web_tool/hw4_data/', 
        success: function(response) { 
            //S08        
            $('#table_S08').DataTable({
                searching: true,
                paging: true,
                info: true,
                scrollX: true,
                scrollY: true,
                data: response.own_S08_dict ,
                columns: [
                { data: 'index', title: "index" },
                { data: 'genome_site', title: "genome_site" },
                { data: 'TTS_intensity', title: "TTS_intensity" },
                { data: 'TTS_upstream_RNA_coverage', title: "TTS_upstream_RNA_coverage" },
                { data: 'TTS_downstream_RNA_coverage', title: "TTS_downstream_RNA_coverage" },
                { data: 'source', title: "source" },
                { data: 'start_site', title: "start_site" },
                { data: 'end_site', title: "end_site" },
                { 
                    "data": null,
                    "title": "Sequence & RNAfold",
                    "render": function(data, type, row) {
                        var combinedText = row.sequence + '<br>' + row.RNAfold;
                        return '<pre style="white-space: pre-wrap; font-family: \'Courier New\', Courier, monospace;">' + combinedText + '</pre>';
                    }
                },
                { data: 'RNAfold_energy', title: "RNAfold_energy" },
                {
                    data: null,
                    title: "Show Picture",
                    render: function (data, type, row) {
                        if (type === 'display') {
                            return '<button type="button" class="btn btn-success Run-btn_S08" data-toggle="modal" data-target="#own_S08_Picture">Picture</button>';
                        } else {
                            return data;
                        }
                    }
                },
                ],
                rowCallback: function (row, data) {
                    $(row).find('.Run-btn_S08').on('click', function () {

                        $.ajax({
                            url: '/web_tool/hw4_S08_plot/', 
                            type: 'POST', 
                            data:  data ,
                            dataType : 'json',
                            success: function (response) {


                                //清空圖像
                                $("#S08_img").attr("src", '');
                                //讀取base64圖片
                                $("#S08_img").attr("src", `data:image/png;base64,${response.img_str}`);
                            
                            },
                            error: function (error) {
                                console.error('Untrack Error:', error);
                            }
                            
                        });
                        
                    });
                },
                destroy: true,
            });


            //S09
            $('#table_S09').DataTable({
                searching: true,
                paging: true,
                info: true,
                scrollX: true,
                scrollY: true,
                data: response.own_S09_dict ,
                columns: [
                { data: 'index', title: "index" },
                { data: 'genome_site', title: "genome_site" },
                { data: 'TTS_intensity', title: "TTS_intensity" },
                { data: 'TTS_upstream_RNA_coverage', title: "TTS_upstream_RNA_coverage" },
                { data: 'TTS_downstream_RNA_coverage', title: "TTS_downstream_RNA_coverage" },
                { data: 'source', title: "source" },
                { data: 'start_site', title: "start_site" },
                { data: 'end_site', title: "end_site" },
                { 
                    "data": null,
                    "title": "Sequence & RNAfold",
                    "render": function(data, type, row) {
                        var combinedText = row.sequence + '<br>' + row.RNAfold;
                        return '<pre style="white-space: pre-wrap; font-family: \'Courier New\', Courier, monospace;">' + combinedText + '</pre>';
                    }
                },
                { data: 'RNAfold_energy', title: "RNAfold_energy" },
                {
                    data: null,
                    title: "Show Picture",
                    render: function (data, type, row) {
                        if (type === 'display') {
                            return '<button type="button" class="btn btn-success Run-btn_S09" data-toggle="modal" data-target="#own_S09_Picture">Picture</button>';
                        } else {
                            return data;
                        }
                    }
                },
                ],
                rowCallback: function (row, data) {
                    $(row).find('.Run-btn_S09').on('click', function () {

                        $.ajax({
                            url: '/web_tool/hw4_S09_plot/', 
                            type: 'POST', 
                            data:  data ,
                            dataType : 'json',
                            success: function (response) {


                                //清空圖像
                                $("#S09_img").attr("src", '');
                                //讀取base64圖片
                                $("#S09_img").attr("src", `data:image/png;base64,${response.img_str}`);
                            
                            },
                            error: function (error) {
                                console.error('Untrack Error:', error);
                            }
                            
                        });
                        
                    });
                },
                destroy: true,
            });
        },
        error: function (error) {
            console.error('Something Error:', error);
        }
    })





})