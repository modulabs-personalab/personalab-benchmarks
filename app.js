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
        return $http.get(url+"?r="+Math.random()).then((response) => {
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
        const scaleDict = { "A": 5, "B": 4, "C": 3, "D": 2, "E": 1 }
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
                console.log(trait); // O, C, E, A, N
                const values = oceanSamples[trait];
                const sum = values.reduce((a, b) => a + b, 0);
                return values.length ? sum / values.length : 0;
            });

            // 레이더 차트를 위한 데이터와 레이아웃
            const data = [{
                    type: 'scatterpolar',
                    r: [3.44, 3.60, 3.41, 3.66, 2.80, 3.44],
                    theta: ['O', 'C', 'E', 'A', 'N', 'O'],
                    fill: 'toself',
                    line: {
                        color: 'rgba(0,0,0,0)' // 선을 투명하게 설정
                    }, 
                    name:"Human",
                },{
                    type: 'scatterpolar',
                    r: [...averages, averages[0]], // 첫 번째 값을 마지막에 추가
                    theta: [...traits, traits[0]], // 첫 번째 값을 마지막에 추가
                    fill: 'toself',
                    name: "LLM"
                } ];

            // 차트 그리기
            Plotly.newPlot('barChart', data,  {
                polar: {
                    radialaxis: {
                        visible: true,
                        range: [-5, 5] // 값을 정규화한 경우, 적절한 범위를 설정
                    }
                },
                title: 'OCEAN Traits Radar Chart',
                legend: {
                    orientation: 'h', // 수평 정렬
                    x: 0.5,           // x축 중앙에 정렬
                    xanchor: 'center',
                    y: -0.2           // 그래프 하단으로 이동
                }
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


