const sample =  [
    {id: 1, name: "mmb", result: "pass", score: 9},
    {id: 2, name: "a chính", result: "fail", score: 5},
    {id: 3, name: "john rod", result: "pass", score: 8},
    {id: 4, name: "họa lớn", result: "fail", score: 4}
]

filtered = [];

for (let i = 0; i < sample.length; i++) {
    if (sample[i].result === "pass") {
        filtered.push(sample[i]);
    }
}

function sumResults(sample) {
    let sum = 0;
    for (let i = 0; i < sample.length; i++) {
        sum += sample[i].score;
    }
    return sum;
}

function highestScore(sample) {
    let highest = sample[0].score;
    for (let i = 1; i < sample.length; i++) {
        if (sample[i].score > highest) {
            highest = sample[i].score;
        }
    }
    return highest;
}