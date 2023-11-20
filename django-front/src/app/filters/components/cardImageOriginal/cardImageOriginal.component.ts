import { Component, Input } from '@angular/core';
import { IndexedImages } from '../../interfaces';

@Component({
  selector: 'app-card-image-original',
  templateUrl: './cardImageOriginal.component.html',
  styles: [``],
})
export class CardImageOriginalComponent {

  @Input({required: true}) image!: IndexedImages;

}
