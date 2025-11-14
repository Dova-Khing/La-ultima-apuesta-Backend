import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService, LoginRequest } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  template: `
    <div class="login-container">
      <div class="login-card">
        <div class="card">
          <div class="card-header text-center">
            <div class="login-icon">[ICONO]</div>
            <h2>Iniciar Sesión</h2>
            <p>Accede a tu cuenta para continuar</p>
          </div>
          
          <div class="card-body">
            <form (ngSubmit)="onSubmit()" #loginForm="ngForm">
              <!-- Credenciales de prueba visibles -->
              <div class="demo-credentials">
                <div class="demo-header">
                  <span class="demo-icon">[ICONO]</span>
                  <strong>Credenciales de Prueba</strong>
                </div>
                <div class="demo-info">
                  <p><strong>Usuario:</strong> admin</p>
                  <p><strong>Contraseña:</strong> admin123</p>
                </div>
              </div>

              <!-- Campo de usuario -->
              <div class="form-group">
                <label for="email" class="form-label">
                  <span class="label-icon">[ICONO]</span>
                  Usuario
                </label>
                <input 
                  type="text" 
                  id="email"
                  class="form-control" 
                  [(ngModel)]="loginData.email"
                  name="email"
                  required
                  placeholder="admin"
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
                  [(ngModel)]="loginData.password"
                  name="password"
                  required
                  placeholder="admin123"
                  #password="ngModel"
                  [class.is-invalid]="password.invalid && password.touched"
                >
              </div>

              <!-- Botón de envío -->
              <div class="form-group">
                <button 
                  type="submit" 
                  class="btn btn-primary w-100"
                  [disabled]="loginForm.invalid || loading"
                  [class.loading]="loading"
                >
                  <span *ngIf="loading">Iniciando sesión...</span>
                  <span *ngIf="!loading">Iniciar Sesión</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    /* Estilos con glass morphism y animaciones */
    .login-container {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 80vh;
      padding: 2rem;
    }
    
    .login-card {
      width: 100%;
      max-width: 450px;
    }

    .card {
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 16px;
      padding: 2rem;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .demo-credentials {
      background: rgba(59, 130, 246, 0.1);
      border: 1px solid rgba(59, 130, 246, 0.2);
      border-radius: 8px;
      padding: 1rem;
      margin: 1.5rem 0;
      text-align: center;
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
export class LoginComponent implements OnInit {
  // Objeto para almacenar los datos del formulario
  loginData: LoginRequest = {
    email: '',
    password: ''
  };
  
  loading = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit(): void {
    // Si ya está autenticado, redirigir al dashboard
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/dashboard']);
    }
  }

  // Método que se ejecuta al enviar el formulario
  onSubmit(): void {
    if (this.loading) return;

    this.loading = true;
    
    // Llamamos al servicio de autenticación
    this.authService.login(this.loginData).subscribe({
      next: (response) => {
        // Si el login es exitoso, guardamos los datos del usuario
        this.authService.setUserData(response.data);
        this.router.navigate(['/dashboard']);
        this.loading = false;
      },
      error: (error) => {
        // Si hay error, mostramos el mensaje
        console.error('Error en login:', error);
        alert('Error al iniciar sesión. Verifica tus credenciales.');
        this.loading = false;
      }
    });
  }
}