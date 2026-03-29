const dropArea = document.getElementById('dropArea');
const fileElem = document.getElementById('fileElem');
const fileSelect = document.getElementById('fileSelect');
const gallery = document.getElementById('gallery');
const legendList = document.getElementById('legendList');

const recoveryBox = document.getElementById("recovery");
const timeBox = document.getElementById("time");
const foodBox = document.getElementById("food");


fileSelect.addEventListener("click", () => fileElem.click());

fileElem.addEventListener("change", (e) => {
handleFiles(e.target.files);
});


dropArea.addEventListener("dragover", (e) => {
e.preventDefault();
});

dropArea.addEventListener("drop", (e) => {

e.preventDefault();

handleFiles(e.dataTransfer.files);

});


async function handleFiles(files){

for(const file of files){

await processFile(file);

}

}


async function processFile(file){

const originalImage = await displayImage(file,"Original");

gallery.appendChild(originalImage);

try{

const reader = new FileReader();

const fileData = await new Promise(resolve =>{

reader.onload = () => resolve(reader.result.split(',')[1]);

reader.readAsDataURL(file);

});


const result = await eel.process_image(fileData)();


if(result){

const processedImage = createImageElement(
`data:image/png;base64,${result.processedImage}`,
"Processed"
);

gallery.appendChild(processedImage);


result.detections.forEach(d =>{

const div = document.createElement("div");

div.innerText = `Detected: ${d.class} | Confidence: ${d.confidence.toFixed(2)}`;

gallery.appendChild(div);

});


recoveryBox.innerText = result.recoveryAdvice;

timeBox.innerText = result.recoveryTime;

foodBox.innerText = result.foodRecommendation;

}

}catch(error){

console.error(error);

}

}


function displayImage(file,label){

return new Promise(resolve =>{

const reader = new FileReader();

reader.onload = e =>{

const img = createImageElement(e.target.result,label);

resolve(img);

};

reader.readAsDataURL(file);

});

}


function createImageElement(src,label){

const container = document.createElement("div");

container.className = "image-container";


const img = document.createElement("img");

img.src = src;


const text = document.createElement("div");

text.className = "image-label";

text.innerText = label;


container.appendChild(img);

container.appendChild(text);


return container;

}


eel.get_class_names()().then(classNames=>{

classNames.forEach(name=>{

const li = document.createElement("li");

li.innerText = name;

legendList.appendChild(li);

});

});