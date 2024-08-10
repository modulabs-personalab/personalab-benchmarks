function tryConvertToNumeric(value) {    
    const numericValue = parseFloat(value);
    return isNaN(numericValue) ? value : numericValue;
}

const app = angular.module('mpi', []);
app.controller('MainCtrl', function ($scope, $http) {
    
    $scope.uiState = {
        selectedReport: "",
        inventory: [],
        loadedReport: null
    }
    $scope.reports = []

    $scope.onClickLoad = async () => {
        
        const report = await $scope.fetchJson(`./results/${$scope.uiState.selectedReport}`);
        
        const inventoryName = report["controls"]["inventory"];
        const tsvStr = await $scope.fetchTsv(`./inventory/${inventoryName}`);
        const lines = tsvStr.replace(/\r/g, "").trim().split('\n');
        const headers = [...lines[0].split('\t'), "LLM Response"];
        console.log(headers);
        const rows = lines.slice(1).map((row, idx) => {
            let values = row.split('\t');
            let found = report.results.filter(e => e.idx == idx)[0];
            values.push(found.answer);
            return values;
        });

        const inventory = { headers, rows };

        // update ui
        $scope.uiState.loadedReport = report;
        $scope.uiState.inventory = inventory;
        $scope.draw_mpi_120_barchart(report, inventory);

        $scope.$digest(); // AngularJS가 변경 사항을 감지하도록 함
    }

    $scope.fetchJson = async (url) => {
        return $http.get(url).then((response) => {
            return response.data;
        });
    }

    $scope.fetchTsv = async (url) => {
        return $http.get(url).then((response) => {
            return response.data;
        });
    }

    $scope.draw_mpi_120_barchart = function (report, inventory) {

        const dict = inventory.rows.map(row=>{
            const item = {}
            for(let col in row){
                const fieldName = inventory.headers[col];
                const fieldValue = tryConvertToNumeric(row[col]);
                item[fieldName] = fieldValue;
            }
            return item;
        });

        const traits = ['O', 'C', 'E', 'A', 'N'];
        const oceanSamples = { "O": [], "C": [], "E": [], "A": [], "N": [] }
        const scaleDict = { "A": 1, "B": 2, "C": 3, "D": 4, "E": 5 }
        for(let i in report.results){
            const e = report.results[i];
            const item = dict[e.idx];
            const ocean = item['label_ocean'].toUpperCase();
            const oneOrMinusOne = item['key'];
            const value = oneOrMinusOne * scaleDict[e.answer];            
            oceanSamples[ocean].push(value);
        }

        // inventory
        console.log(report);
        console.log(inventory);
        console.log(dict);
        console.log(oceanSamples);

        let drawRadar = ()=>{
            // 각 성격 특성의 평균 계산
            const averages = traits.map(trait => {
                const values = oceanSamples[trait];
                const sum = values.reduce((a, b) => a + b, 0);
                return values.length ? sum / values.length : 0;
            });

            // 레이더 차트를 위한 데이터와 레이아웃
            const data = [{
                    type: 'scatterpolar',
                    r: averages,
                    theta: traits,
                    fill: 'toself'
                }];

            // 차트 그리기
            Plotly.newPlot('barChart', data,  {
                polar: {
                    radialaxis: {
                        visible: true,
                        range: [-5, 5] // 값을 정규화한 경우, 적절한 범위를 설정
                    }
                },
                title: 'OCEAN Traits Radar Chart'
            });
        }
        
        let drawBox = ()=>{
            const data = traits.map(trait => ({
                y: oceanSamples[trait],
                type: 'box',
                name: trait
            }));
    
            // 차트 그리기
            Plotly.newPlot('boxPlot', data, {
                title: 'OCEAN Traits Box Plot',
                yaxis: {
                    title: 'Values',
                    range: [-5, 5] // 값을 정규화한 경우, 적절한 범위를 설정
                },
                xaxis: {
                    title: 'Traits'
                }
            });
        }
        
        drawRadar()
        drawBox()
    }

    $scope.run  = async () => {
        // console.error('No TSV file URL provided in query parameters.');
        const reports = await $scope.fetchJson('./index.json');
        $scope.reports = reports;
        // console.log(reports);   
        $scope.$digest(); // AngularJS가 변경 사항을 감지하도록 함
    }

    // URL 쿼리 매개변수에서 TSV 파일 경로 추출
    $scope.run();
});


