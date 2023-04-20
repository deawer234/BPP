
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.module.js';
import { OrbitControls } from "https://unpkg.com/three@0.112/examples/jsm/controls/OrbitControls.js";
import { appendToEventLog }from "./logger.js";

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

// const sphereGeometry = new THREE.SphereGeometry(332, 32, 32, 0, 2* Math.PI, 0, Math.PI);
// const sphereMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff, opacity: 0.1, transparent: true });
// const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
// scene.add(sphere);

const axesHelper = new THREE.AxesHelper(800);
scene.add(axesHelper);

function createArmSegment(length, color) {
const geometry = new THREE.CylinderGeometry(5, 5, length, 32);
const material = new THREE.MeshStandardMaterial({ color: color });
const segment = new THREE.Mesh(geometry, material);
segment.position.y = length / 2;
return segment;
}

// Create a robotic arm model with a base, shoulder, elbow, and wrist
const base = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 0.5, 32), new THREE.MeshStandardMaterial({ color: 0xffffff }));
base.position.y = 0.25;
scene.add(base);

const shoulder = createArmSegment(120, 0xff0000);
const shoulderPivot = new THREE.Object3D();
shoulderPivot.position.y = 0.5;
shoulderPivot.add(shoulder);
base.add(shoulderPivot);

const elbow = createArmSegment(88, 0x00ff00);
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
//base.rotation.y = baseAngle;
shoulderPivot.rotation.set(0, baseAngle, shoulderAngle, 'YZX');
elbowPivot.rotation.set(0, 0, elbowAngle, 'ZYX');
wristPivot.rotation.set(0, 0, wristAngle, 'ZYX');
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
        setArmRotation(response.base, response.shoulder, response.elbow, response.wrist);
        document.getElementById("base").value = response.base;
        document.getElementById("shoulder").value = (response.shoulder + 24);
        document.getElementById("elbow").value = (response.elbow + 121);
        document.getElementById("wrist").value = (response.wrist + 90);
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
      'wrist': $('#wrist').val() - 90,
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
      'wrist': $('#wrist').val() - 90,
      'wrist_rot': $('#wrist_rot').val(),
      'gripper': $('#gripper').val()
    };
    setArmRotation(data.base, data.shoulder, data.elbow, data.wrist);

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
          setArmRotation(response.base, response.shoulder, response.elbow, response.wrist);
        }
      }
    });

  });
});