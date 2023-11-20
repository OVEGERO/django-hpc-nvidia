import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environments } from 'src/environments/environment.prod';
import { FilterResponse, ImageRequest } from '../interfaces';

@Injectable({
  providedIn: 'root',
})
export class FiltersService {
  private baseUrl: string = environments.baseUrl;

  constructor(private httpClient: HttpClient) {}

  makeConvolution(imageRequest: ImageRequest): Observable<FilterResponse> {
    const formData: FormData = new FormData();
    formData.append('image', imageRequest.image);
    formData.append('filter_name', imageRequest.filter_name);
    formData.append('sigma', imageRequest.sigma.toString());
    formData.append('kernel_size', imageRequest.kernel_size.toString());

    return this.httpClient.post<FilterResponse>(`${this.baseUrl}`, formData);
  }

}
