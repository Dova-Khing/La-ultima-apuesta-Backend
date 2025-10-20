import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';

// Interface para definir la estructura de un producto
interface Producto {
  id: number;
  nombre: string;
  descripcion: string;
  precio: number;
  categoria: string;
  stock: number;
  fechaCreacion: string;
}

@Component({
  selector: 'app-producto-list',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './usuario-list.component.html',
  styleUrls: ['./usuario-list.component.scss']
})
export class ProductoListComponent implements OnInit {
  
  // Array con datos de ejemplo de productos
  productos: Producto[] = [
    {
      id: 1,
      nombre: 'Laptop Dell Inspiron',
      descripcion: 'Laptop para trabajo y entretenimiento',
      precio: 2500000,
      categoria: 'Tecnología',
      stock: 15,
      fechaCreacion: '2025-01-15'
    },
    {
      id: 2,
      nombre: 'Mouse Inalámbrico',
      descripcion: 'Mouse óptico inalámbrico ergonómico',
      precio: 85000,
      categoria: 'Accesorios',
      stock: 50,
      fechaCreacion: '2025-01-14'
    },
    {
      id: 3,
      nombre: 'Teclado Mecánico',
      descripcion: 'Teclado mecánico RGB para gaming',
      precio: 320000,
      categoria: 'Accesorios',
      stock: 25,
      fechaCreacion: '2025-01-13'
    },
    {
      id: 4,
      nombre: 'Monitor 24"',
      descripcion: 'Monitor Full HD para oficina',
      precio: 450000,
      categoria: 'Monitores',
      stock: 12,
      fechaCreacion: '2025-01-12'
    },
    {
      id: 5,
      nombre: 'Auriculares Bluetooth',
      descripcion: 'Auriculares inalámbricos con cancelación de ruido',
      precio: 180000,
      categoria: 'Audio',
      stock: 30,
      fechaCreacion: '2025-01-11'
    },
    {
      id: 6,
      nombre: 'Tablet Samsung',
      descripcion: 'Tablet Android para trabajo y entretenimiento',
      precio: 1200000,
      categoria: 'Tecnología',
      stock: 8,
      fechaCreacion: '2025-01-10'
    }
  ];

  constructor() { }

  ngOnInit() {
    // Lógica de inicialización si es necesaria
  }

  // Método para formatear precios en pesos colombianos
  formatearPrecio(precio: number): string {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 0
    }).format(precio);
  }

  // Método para crear un nuevo producto
  crearProducto() {
    console.log('Crear nuevo producto');
    // Aquí se implementaría la lógica para crear un nuevo producto
    alert('Función de crear producto - Por implementar');
  }

  // Método para editar un producto existente
  editarProducto(producto: Producto) {
    console.log('Editar producto:', producto);
    // Aquí se implementaría la lógica para editar un producto
    alert(`Editando producto: ${producto.nombre}`);
  }

  // Método para eliminar un producto
  eliminarProducto(producto: Producto) {
    console.log('Eliminar producto:', producto);
    // Aquí se implementaría la lógica para eliminar un producto
    if (confirm(`¿Estás seguro de eliminar ${producto.nombre}?`)) {
      alert(`Producto ${producto.nombre} eliminado`);
    }
  }
}