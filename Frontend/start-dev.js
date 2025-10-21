#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

console.log('🚀 Iniciando servidor de desarrollo Angular...\n');

// Configuración del servidor
const ngServe = spawn('ng', ['serve', '--open', '--host', '0.0.0.0', '--port', '4200'], {
  stdio: 'pipe',
  shell: true,
  cwd: process.cwd()
});

// Mostrar URL cuando el servidor esté listo
ngServe.stdout.on('data', (data) => {
  const output = data.toString();
  console.log(output);
  
  // Detectar cuando el servidor está listo
  if (output.includes('Local:') || output.includes('Network:')) {
    console.log('\n' + '='.repeat(60));
    console.log('🎉 ¡Servidor Angular iniciado exitosamente!');
    console.log('='.repeat(60));
    console.log('🌐 URL Local:    http://localhost:4200');
    console.log('🌍 URL Red:      http://0.0.0.0:4200');
    console.log('📱 Acceso móvil: http://[tu-ip]:4200');
    console.log('='.repeat(60));
    console.log('💡 Presiona Ctrl+C para detener el servidor\n');
  }
});

ngServe.stderr.on('data', (data) => {
  console.error('Error:', data.toString());
});

ngServe.on('close', (code) => {
  console.log(`\n🔴 Servidor detenido con código: ${code}`);
});

// Manejar Ctrl+C
process.on('SIGINT', () => {
  console.log('\n🛑 Deteniendo servidor...');
  ngServe.kill('SIGINT');
  process.exit(0);
});

process.on('SIGTERM', () => {
  ngServe.kill('SIGTERM');
  process.exit(0);
});