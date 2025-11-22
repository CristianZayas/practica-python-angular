import { Component, OnDestroy, OnInit, signal } from '@angular/core';
import { ConfirmationService, MessageService, SelectItem } from 'primeng/api';
import { TableModule } from 'primeng/table';
import { ToastModule } from 'primeng/toast';
import { CommonModule } from '@angular/common';
import { TagModule } from 'primeng/tag';
import { SelectModule } from 'primeng/select';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { DialogModule } from 'primeng/dialog';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { UserServices } from '../../services/user';

@Component({
  selector: 'app-user',
  imports: [TableModule, ReactiveFormsModule, ConfirmDialogModule, DialogModule, FormsModule, ToastModule, CommonModule, TagModule, SelectModule, ButtonModule, InputTextModule],
  templateUrl: './user.html',
  styleUrl: './user.css',
  providers: [MessageService, ConfirmationService]
})
export class User implements OnInit, OnDestroy {
 public formUser : FormGroup = new FormGroup({})
  visible: boolean = false;
  public users = signal<any>([]);

  statuses!: SelectItem[];

  clonedProducts: { [s: string]: any } = {};

  constructor(private fb: FormBuilder,private messageService: MessageService, private confirmationService: ConfirmationService, private readonly UserService: UserServices) { 
    this.formUser = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(1), Validators.maxLength(100)]],
      description: ['', [Validators.required, Validators.minLength(1), Validators.maxLength(400)]]
    });
  }
  ngOnDestroy(): void {
    //throw new Error('Method not implemented.');
  }

  ngOnInit() {
    this.UserService.getUser().subscribe({
      next: (result) => {
        this.users.set(result);
      }, error: (error) => {
        console.log(error)
      }
    })
  }

  loaderData(){
    this.UserService.getUser().subscribe({
      next: (result) => {
        this.users.set(result);
      },
      error: (error) => {
        console.log(error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error al cargar usuarios',
          detail: 'No se pudieron obtener los datos. Verifica la conexión con el servidor.'
        });
      }
    });
    
  }


  showDialog() {
    this.visible = true;
  }
  onRowEditInit(product: any) {
    this.clonedProducts[product.id as string] = { ...product };
  }



  deleteUser(id: number) {
    console.log(id);
    this.confirm2(id);
  }

  confirm2(id: number) {
    this.confirmationService.confirm({
      message: '¿Deseas eliminar este usuario?',
      header: 'Zona de Peligro',
      icon: 'pi pi-info-circle',

      rejectLabel: 'Cancelar',
      rejectButtonProps: {
        label: 'Cancelar',
        severity: 'secondary',
        outlined: true,
      },

      acceptButtonProps: {
        label: 'Eliminar',
        severity: 'danger',
      },

      accept: () => {
        this.UserService.UserDelete(String(id)).subscribe({
          next: () => {
            this.messageService.add({
              severity: 'success',
              summary: 'Usuario eliminado',
              detail: 'El usuario ha sido eliminado correctamente.'
            });
           this.loaderData();
            // Recargar la lista de usuarios después de eliminar
          },
        
          error: (error : any) => {
            console.log(error);
            this.messageService.add({
              severity: 'error',
              summary: 'Error al eliminar usuario',
              detail: 'No se pudo eliminar el usuario. Verifica la conexión con el servidor.'
            });
          }
        });

        
        
      },

      reject: () => {
        this.messageService.add({
          severity: 'error',
          summary: 'Acción cancelada',
          detail: 'La eliminación ha sido cancelada'
        });
      },
    });

  }
  onRowEditSave(user: any) {
     this.UserService.UserUpdate(String(user.id), user).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Usuario actualizado',
          detail: 'El usuario ha sido actualizado correctamente.'
        });
    
        // Recargar la lista de usuarios después de actualizar
        this.loaderData();
      },
    
      error: (error: any) => {
        console.log(error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error al actualizar usuario',
          detail: 'No se pudo actualizar el usuario. Verifica la conexión con el servidor.'
        });
      }
    });
    
  }

  onRowEditCancel(product: any, index: number) {
    this.users()[index] = this.clonedProducts[product.id as string];
    delete this.clonedProducts[product.id as string];
  }

  send(){
    this.UserService.newUser(this.formUser.value).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Usuario creado',
          detail: 'El usuario ha sido registrado correctamente.'
        });
        this.visible =  false;
        // Recargar la lista de usuarios después de crear
        this.loaderData();
      },
    
      error: (error: any) => {
        console.log(error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error al crear usuario',
          detail: 'No se pudo registrar el usuario. Verifica la conexión con el servidor.'
        });
      }
    });
    
  }

}
