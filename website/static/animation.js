
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.module.js';
import { OrbitControls } from "https://unpkg.com/three@0.112/examples/jsm/controls/OrbitControls.js";
import { appendToEventLog }from "./logger.js";
import { SimplifyModifier } from 'https://unpkg.com/three@0.112/examples/jsm/modifiers/SimplifyModifier.js';
import { STLLoader } from 'https://unpkg.com/three@0.112/examples/jsm/loaders/STLLoader.js';

const viewer = document.getElementById('viewer');
const scene = new THREE.Scene();
scene.background = new THREE.Color( 0xD3D3D3);
const camera = new THREE.PerspectiveCamera(75, viewer.clientWidth / viewer.clientHeight, 0.1, 10000);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(viewer.clientWidth, viewer.clientHeight);
viewer.appendChild(renderer.domElement);

const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const controls = new OrbitControls(camera, renderer.domElement);
camera.position.set(300, 300, 450);
camera.lookAt(scene.position);


// Create and add Z-axis grid (blue)
const zAxisGrid = new THREE.GridHelper(1000,10, 0xffffff, 0xffffff);
zAxisGrid.position.set(0, 0, 0);
scene.add(zAxisGrid);

async function loadArmModel(modelUrl, color) {
  return new Promise((resolve, reject) => {
    const loader = new STLLoader();

    loader.load(modelUrl, (geometry) => {
    
    
      const material = new THREE.MeshStandardMaterial({ color: color });
      const model = new THREE.Mesh(geometry, material);
      // Compute the bounding box
      const bbox = new THREE.Box3().setFromObject(model);

      // Calculate the dimensions of the model
      const dimensions = new THREE.Vector3();
      bbox.getSize(dimensions);
      console.log('Model dimensions:', dimensions);
                      // Create an edges geometry from the loaded geometry
      const edgesGeometry = new THREE.EdgesGeometry(geometry, 30);

      // Create a wireframe material
      const wireframeMaterial = new THREE.LineBasicMaterial({ color: 0x000000 });

      // Create a line segments object using the edges geometry and wireframe material
      const wireframe = new THREE.LineSegments(edgesGeometry, wireframeMaterial);

      // Add the wireframe to the model
      model.add(wireframe);
      resolve(model);
    }, undefined, (error) => {
      reject(error);
    });
  });
}


const axesHelper = new THREE.AxesHelper(800);
scene.add(axesHelper);

function createArmSegmentWithModel(model, pivotOffset, rotation, scale) {
    model.position.y = pivotOffset/2;
    model.rotation.set(rotation.x, rotation.y, rotation.z);
    //model.scale.set(scale.x, scale.y, scale.z);
  return model;
}
const baseBaseModel = await loadArmModel("../static/basebase.stl", 0xffffff);
const baseModel = await loadArmModel("../static/base.stl", 0x0000ff);
const shoulderModel = await loadArmModel("../static/shoulder.stl", 0x0000ff);
const elbowModel = await loadArmModel("../static/elbow.stl", 0x0000ff);
const wristModel = await loadArmModel("../static/wrist.stl", 0x0000ff);
const endEffector = await loadArmModel("../static/endeffector.stl", 0xffffff)

const baseBase = createArmSegmentWithModel(baseBaseModel, 100, { x: 0, y: 0, z: 0 }, { x: 1000, y: 1000, z: 1000 });
const baseP = createArmSegmentWithModel(baseModel, 1, { x: - Math.PI/2 , y: 0, z: Math.PI/2 }, { x: 1000, y: 1000, z: 1000 });
//const shoulder = createArmSegmentWithModel(shoulderModel, 120, { x: Math.PI / 2, y: 0, z: 0 }, { x: 1000, y: 1000, z: 1000 });
//const elbow = createArmSegmentWithModel(elbowModel, 88, { x: 0, y: 0, z: 0 }, { x: 1000, y: 1000, z: 1000 });
//const wrist = createArmSegmentWithModel(wristModel, 124, { x: 0, y: 0, z: 0 }, { x: 1000, y: 1000, z: 1000 });


function createArmSegment(length, color) {
  const geometry = new THREE.CylinderGeometry(5, 5, length, 32);
  const material = new THREE.MeshStandardMaterial({ color: color });
  const segment = new THREE.Mesh(geometry, material);
  segment.position.y = length / 2;
  return segment;
  }
  
  // Create a robotic arm model with a base, shoulder, elbow, and wrist
  const base = new THREE.Object3D();
  base.position.y = -50;
  base.add(baseBase);
  scene.add(base);

  const basePivot = new THREE.Object3D();
  basePivot.position.y = 100;
  basePivot.add(baseP);
  scene.add(basePivot)
  //base.add(basePivot);

  const shoulder = createArmSegmentWithModel(shoulderModel, 120, { x: Math.PI/2, y: Math.PI/2, z: 0 }, { x: 1000, y: 1000, z: 1000 });
  shoulder.position.set(-18, 0, 0)
  const shoulderPivot = new THREE.Object3D()
  shoulderPivot.position.y = 44;
  shoulderPivot.rotation.set(0, 0, 0)
  shoulderPivot.add(shoulder);
  basePivot.add(shoulderPivot);
  
  const elbow = createArmSegmentWithModel(elbowModel, 88, { x: 0, y: Math.PI, z: Math.PI/2 }, { x: 1000, y: 1000, z: 1000 });
  elbow.position.set(0, 0, -2)
  const elbowPivot = new THREE.Object3D()
  elbowPivot.position.y = 120;
  elbowPivot.rotation.set(0,0,0)
  elbowPivot.add(elbow);
  shoulderPivot.add(elbowPivot);
  
  const wrist = createArmSegmentWithModel(wristModel, 100, { x: 0, y: 0, z: Math.PI/2 }, { x: 1000, y: 1000, z: 1000 });
  wrist.position.set(0, 0, 2)
  const wristPivot = new THREE.Object3D()
  wristPivot.position.y = 88;
  wristPivot.add(wrist);
  elbowPivot.add(wristPivot);

  const endeffector = createArmSegmentWithModel(endEffector, 100, { x: 0, y: 0, z: Math.PI/2 }, { x: 1000, y: 1000, z: 1000 });
  endeffector.position.set(24, -50, 8)
  const effectorPivot = new THREE.Object3D()
  effectorPivot.position.y = 100;
  effectorPivot.add(endEffector);
  wristPivot.add(effectorPivot);


  function degreesToRadians(degrees) {
  return degrees * (Math.PI / 180);
  }
  
  export function setArmRotation(baseAngle, shoulderAngle, elbowAngle, wristAngle, effectorAngle) {
  // Convert angles from degrees to radians
  baseAngle = degreesToRadians(baseAngle);
  console.log(shoulderAngle)
  shoulderAngle = degreesToRadians(shoulderAngle - 90);
  elbowAngle = degreesToRadians(elbowAngle);
  wristAngle = degreesToRadians(wristAngle);
  effectorAngle = degreesToRadians(effectorAngle - 90);
  
  // Set the rotations
  basePivot.rotation.y = baseAngle;
  shoulderPivot.rotation.z = shoulderAngle;
  //shoulder.rotation.set(0, 0, shoulderAngle, 'ZYX');
  elbowPivot.rotation.z = elbowAngle;
  wristPivot.rotation.z = wristAngle;
  effectorPivot.rotation.y = effectorAngle;
  }


function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

animate();

function moveArm(data) {
  $.ajax({
    type: "POST",
    url: "/move",
    contentType: "application/json",
    data: JSON.stringify(data),
    success: function(response) {
      console.log(response);
    
      if(typeof response === 'string')
        appendToEventLog(response);
      else{
        appendToEventLog("Arm in place")
        setArmRotation(response.base, response.shoulder, response.elbow, response.wrist, response.wrist_rot);
        document.getElementById("base").value = response.base;
        document.getElementById("shoulder").value = (response.shoulder + 24);
        document.getElementById("elbow").value = (response.elbow + 121);
        document.getElementById("wrist").value = (response.wrist + 115);
        document.getElementById("wrist_rot").value = response.wrist_rot;
        document.getElementById("gripper").value = response.gripper;
      }
    }
  });
}

$(document).ready(function() {
  $("#submit-btn").click(function() {
    const z = parseFloat($("#z").val()) + 144
    var data = {
      "x": $("#x").val(),
      "y": $("#y").val(),
      "z": $("#z").val()
    };
    appendToEventLog("Moving to the coordinates...")
    moveArm(data);
  });

  $('#move-btn').click(function() {
    var data = {
      'base': $('#base').val(),
      'shoulder': $('#shoulder').val() - 24,
      'elbow': $('#elbow').val() - 121,
      'wrist': $('#wrist').val() - 115,
      'wrist_rot': $('#wrist_rot').val(),
      'gripper': $('#gripper').val()
    };
    appendToEventLog("Moving to new angles...")
    moveArm(data);
  });

  $('input[type=number]').on('input', function() {

    var data = {
      'base': $('#base').val(),
      'shoulder': $('#shoulder').val() - 24,
      'elbow': $('#elbow').val() - 121,
      'wrist': $('#wrist').val() - 115,
      'wrist_rot': $('#wrist_rot').val(),
      'gripper': $('#gripper').val()
    };
    setArmRotation(data.base, data.shoulder, data.elbow, data.wrist, data.wrist_rot);

  });

  
  $('input[type=range]').on('input', function() {

    var data = {
      'base': $('#base').val(),
      'shoulder': $('#shoulder').val() - 24,
      'elbow': $('#elbow').val() - 121,
      'wrist': $('#wrist').val() - 115,
      'wrist_rot': $('#wrist_rot').val(),
      'gripper': $('#gripper').val()
    };
    setArmRotation(data.base, data.shoulder, data.elbow, data.wrist, data.wrist_rot);

  });

  $('#display-btn').click(function() {
    const z = parseFloat($("#z").val()) + 144
    var data = {
      "x": $("#x").val(),
      "y": $("#y").val(),
      "z": $("#z").val()
    };
    appendToEventLog("Displaying selected coordinates position...")
    $.ajax({
      type: "POST",
      url: "/display",
      contentType: "application/json",
      data: JSON.stringify(data),
      success: function(response) {
        console.log(response);
        if(typeof response === 'string')
          appendToEventLog("The position is unreachable");
        else{
          setArmRotation(response.base, response.shoulder, response.elbow, response.wrist, response.wrist_rot);
        }
      }
    });

  });
});