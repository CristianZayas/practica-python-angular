import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class UserServices {
  private https = inject(HttpClient);

  getUser(): Observable<any> {
    return this.https.get('http://localhost:8000/usuarios/');
  }
  newUser( body: any): Observable<any> {
    return this.https.post('http://localhost:8000/usuarios/', body);
  }
  UserUpdate(id: string, body: any): Observable<any> {
    return this.https.put('http://localhost:8000/usuarios/'+id , body);
  }
  UserDelete(id: string): Observable<any> {
    return this.https.delete('http://localhost:8000/usuarios/'+id);
  }

}
