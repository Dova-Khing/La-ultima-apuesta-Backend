import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';

// Interface para definir las rutas del menú
declare interface RouteInfo {
    path: string;
    title: string;
    icon: string;
    class: string;
}

// Array con todas las rutas del sidebar
export const ROUTES: RouteInfo[] = [
    { path: '/dashboard', title: 'Dashboard',  icon: 'design_app', class: '' },
    { path: '/boletos', title: 'Boletos',  icon:'shopping_basket', class: '' },
    { path: '/usuarios', title: 'Usuarios',  icon:'users_single-02', class: '' },
    { path: '/juegos', title: 'Juegos',  icon:'shopping_box', class: '' },
    { path: '/historia_saldo', title: 'Historial_Saldo',  icon:'ui-1_bell-53', class: '' },
    { path: '/premios', title: 'Premios',  icon:'ui-1_bell-53', class: '' },
    { path: '/partidas', title: 'Partidas',  icon:'ui-1_bell-53', class: '' },
];

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
  // Array que contendrá los elementos del menú
  menuItems: any[] = [];

  constructor() { }

  ngOnInit() {
    // Cargar las rutas en el array del menú
    this.menuItems = ROUTES.filter(menuItem => menuItem);
  }
  
  // Método para detectar si es móvil
  isMobileMenu() {
      if ( window.innerWidth > 991) {
          return false;
      }
      return true;
  };
}