import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule],
  template: `
    <div class="register-container">
      <div class="register-card">
        <div class="card">
          <div class="card-header text-center">
            <div class="register-icon">[ICONO]</div>
            <h2>Crear Cuenta</h2>
            <p>Únete a nuestro sistema</p>
          </div>
          
          <div class="card-body">
            <form (ngSubmit)="onSubmit()" #registerForm="ngForm">
              <!-- Campo de email -->
              <div class="form-group">
                <label for="email" class="form-label">
                  <span class="label-icon">[ICONO]</span>
                  Email
                </label>
                <input 
                  type="email" 
                  id="email"
                  class="form-control" 
                  [(ngModel)]="registerData.email"
                  name="email"
                  required
                  email
                  placeholder="tu@email.com"
                  #email="ngModel"
                  [class.is-invalid]="email.invalid && email.touched"
                >
              </div>

              <!-- Campo de contraseña -->
              <div class="form-group">
                <label for="password" class="form-label">
                  <span class="label-icon">[ICONO]</span>
                  Contraseña
                </label>
                <input 
                  type="password" 
                  id="password"
                  class="form-control" 
                  [(ngModel)]="registerData.password"
                  name="password"
                  required
                  minlength="6"
                  placeholder="••••••••"
                  #password="ngModel"
                  [class.is-invalid]="password.invalid && password.touched"
                >
              </div>

              <!-- Campo de nombre -->
              <div class="form-group">
                <label for="nombre" class="form-label">
                  <span class="label-icon">[ICONO]</span>
                  Nombre
                </label>
                <input 
                  type="text" 
                  id="nombre"
                  class="form-control" 
                  [(ngModel)]="registerData.nombre"
                  name="nombre"
                  required
                  minlength="2"
                  placeholder="Tu nombre"
                  #nombre="ngModel"
                  [class.is-invalid]="nombre.invalid && nombre.touched"
                >
              </div>

              <!-- Campo de apellido -->
              <div class="form-group">
                <label for="apellido" class="form-label">
                  <span class="label-icon">[ICONO]</span>
                  Apellido
                </label>
                <input 
                  type="text" 
                  id="apellido"
                  class="form-control" 
                  [(ngModel)]="registerData.apellido"
                  name="apellido"
                  required
                  minlength="2"
                  placeholder="Tu apellido"
                  #apellido="ngModel"
                  [class.is-invalid]="apellido.invalid && apellido.touched"
                >
              </div>

              <!-- Botón de envío -->
              <div class="form-group">
                <button 
                  type="submit" 
                  class="btn btn-primary w-100"
                  [disabled]="registerForm.invalid || loading"
                  [class.loading]="loading"
                >
                  <span *ngIf="loading">Registrando...</span>
                  <span *ngIf="!loading">Crear Cuenta</span>
                </button>
              </div>

              <!-- Enlace al login -->
              <div class="form-options">
                <div class="text-center">
                  <span class="login-text">¿Ya tienes cuenta? </span>
                  <a routerLink="/auth/login" class="link">
                    Inicia sesión aquí
                  </a>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    /* Estilos consistentes con el login */
    .register-container {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 80vh;
      padding: 2rem;
    }
    
    .register-card {
      width: 100%;
      max-width: 500px;
    }

    .card {
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 16px;
      padding: 2rem;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .form-control {
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 8px;
      padding: 0.75rem;
      color: white;
      transition: all 0.3s ease;
    }

    .form-control:focus {
      background: rgba(255, 255, 255, 0.15);
      border-color: #3b82f6;
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
      transform: translateY(-2px);
    }

    .btn {
      background: linear-gradient(135deg, #3b82f6, #1d4ed8);
      border: none;
      border-radius: 8px;
      padding: 0.75rem 1.5rem;
      color: white;
      font-weight: 600;
      transition: all 0.3s ease;
    }

    .btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
    }
  `]
})
export class RegisterComponent implements OnInit {
  // Objeto para almacenar los datos del formulario
  registerData = {
    email: '',
    password: '',
    nombre: '',
    apellido: ''
  };
  
  loading = false;

  constructor(private router: Router) { }

  ngOnInit(): void {
    // Lógica de inicialización si es necesaria
  }

  // Método que se ejecuta al enviar el formulario
  onSubmit(): void {
    if (this.loading) return;

    this.loading = true;
    
    // Simulamos el registro (en un sistema real, aquí se haría la llamada al backend)
    setTimeout(() => {
      console.log('Datos de registro:', this.registerData);
      alert('Registro simulado exitoso. Redirigiendo al login...');
      this.router.navigate(['/auth/login']);
      this.loading = false;
    }, 1500);
  }
}