
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.module.js';
import { OrbitControls } from "https://unpkg.com/three@0.112/examples/jsm/controls/OrbitControls.js";
import { appendToEventLog }from "./logger.js";
import { GLTFLoader } from "https://unpkg.com/three@0.112/examples/jsm/loaders/GLTFLoader.js";

const viewer = document.getElementById('viewer');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, viewer.clientWidth / viewer.clientHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(viewer.clientWidth, viewer.clientHeight);
viewer.appendChild(renderer.domElement);

const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const controls = new OrbitControls(camera, renderer.domElement);
camera.position.set(300, 300, 450);
camera.lookAt(scene.position);
  // Create and add X-axis grid (red)
// const xAxisGrid = new THREE.GridHelper(800, 10, 0xff0000, 0xff0000);
// xAxisGrid.rotation.x = Math.PI / 2;
// xAxisGrid.position.set(0, 0, 0);
// scene.add(xAxisGrid);

// // Create and add Y-axis grid (green)
// const yAxisGrid = new THREE.GridHelper(800, 10, 0x00ff00, 0x00ff00);
// yAxisGrid.rotation.z = Math.PI / 2;
// yAxisGrid.position.set(0, 0, 0);
// scene.add(yAxisGrid);

// Create and add Z-axis grid (blue)
const zAxisGrid = new THREE.GridHelper(800,10, 0xffffff, 0xffffff);
zAxisGrid.position.set(0, 0, 0);
scene.add(zAxisGrid);

async function loadArmModel(modelUrl) {
  return new Promise((resolve, reject) => {
    const loader = new GLTFLoader();
    loader.load(modelUrl, (gltf) => {
      // Update materials to be compatible with the current Three.js version
      gltf.scene.traverse((child) => {
        if (child.isMesh) {
          child.material = new THREE.MeshStandardMaterial({
            map: child.material.map,
            color: child.material.color,
            roughness: child.material.roughness,
            metalness: child.material.metalness,
            envMap: child.material.envMap,
          });
        }
      });
      resolve(gltf.scene);
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
    model.scale.set(scale.x, scale.y, scale.z);
  return model;
}
const baseBaseModel = await loadArmModel("../static/basebase.gltf");
const baseModel = await loadArmModel("../static/base.gltf");
const shoulderModel = await loadArmModel("../static/shoulder.gltf");
const elbowModel = await loadArmModel("../static/elbow.gltf");
const wristModel = await loadArmModel("../static/wrist.gltf");

const baseBase = createArmSegmentWithModel(baseBaseModel, 100, { x: 0, y: 0, z: 0 }, { x: 1000, y: 1000, z: 1000 });
const baseP = createArmSegmentWithModel(baseModel, 67, { x: 0 , y: 0, z: 0  }, { x: 1000, y: 1000, z: 1000 });
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
  base.add(basePivot);

  const shoulder = createArmSegmentWithModel(shoulderModel, 162, { x: Math.PI / 2, y: Math.PI / 2, z: 0 }, { x: 1000, y: 1000, z: 1000 });
  //const shoulder = createArmSegment(120, 0x00ff00);
  const shoulderPivot = new THREE.Object3D();
  shoulderPivot.position.y = 86;
  shoulderPivot.position.x = -86;
  shoulderPivot.add(shoulder);
  basePivot.add(shoulderPivot);
  
  const elbow = createArmSegment(88, 0xff0000);
  //const elbow = createArmSegmentWithModel(elbowModel, 88, { x: 0, y: 0, z: Math.PI/2 }, { x: 1000, y: 1000, z: 1000 });
  const elbowPivot = new THREE.Object3D();
  elbowPivot.position.y = 120;
  elbowPivot.add(elbow);
  shoulderPivot.add(elbowPivot);
  
  const wrist = createArmSegment(124, 0x0000ff);
  const wristPivot = new THREE.Object3D();
  wristPivot.position.y = 88;
  wristPivot.add(wrist);
  elbowPivot.add(wristPivot);
  
  function degreesToRadians(degrees) {
  return degrees * (Math.PI / 180);
  }
  
  export function setArmRotation(baseAngle, shoulderAngle, elbowAngle, wristAngle) {
  // Convert angles from degrees to radians
  baseAngle = degreesToRadians(baseAngle);
  console.log(shoulderAngle)
  shoulderAngle = degreesToRadians(shoulderAngle - 90);
  elbowAngle = degreesToRadians(elbowAngle);
  wristAngle = degreesToRadians(wristAngle);
  
  // Set the rotations
  basePivot.rotation.y = baseAngle;
  shoulderPivot.rotation.set(0, 0, shoulderAngle, 'YZX');
  elbowPivot.rotation.set(0, 0, elbowAngle, 'ZYX');
  wristPivot.rotation.set(0, 0, wristAngle, 'ZYX');
  }

export async function initAndAnimate(baseAngle, shoulderAngle, elbowAngle, wristAngle) {
  // Call setArmRotation here
  setArmRotation(baseAngle, shoulderAngle, elbowAngle, wristAngle);
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
        initAndAnimate(response.base, response.shoulder, response.elbow, response.wrist);
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

  $('input[type=range]').change(function() {

    var data = {
      'base': $('#base').val(),
      'shoulder': $('#shoulder').val() - 24,
      'elbow': $('#elbow').val() - 121,
      'wrist': $('#wrist').val() - 115,
      'wrist_rot': $('#wrist_rot').val(),
      'gripper': $('#gripper').val()
    };
    initAndAnimate(data.base, data.shoulder, data.elbow, data.wrist);

  });

  $('#display-btn').click(function() {
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
          appendToEventLog("The position is outside of arm's workspace or is unreachable");
        else{
          initAndAnimate(response.base, response.shoulder, response.elbow, response.wrist);
        }
      }
    });

  });
});