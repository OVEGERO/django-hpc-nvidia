import { Component, OnInit } from '@angular/core';
import { MessageService } from 'primeng/api';
import { DropdownChangeEvent, Filter, ImagesSrcOut, IndexedImages, InputNumberInputEvent } from '../../interfaces';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styles: [],
  providers: [MessageService],
})
export class MainPageComponent implements OnInit {

  kernel: number = 1;
  sigma: number = 1;

  public filters: Filter[] | undefined;

  public selectedFilter: Filter | undefined;

  public imageSrcOut!: ImagesSrcOut;

  public imageConvIn!: IndexedImages;

  public canUpload: boolean = false;

  public isMedian: boolean = false;

  public isLoading: boolean = false;

  constructor() {}

  ngOnInit() {
    this.filters = [{ name: 'Gaussian' }, { name: 'Median' }, { name: 'Dog' }];
  }

  oddValues(event: InputNumberInputEvent) {
    Number.parseInt(event.value) % 2 == 0 ? ++this.kernel : this.kernel;
  }

  onBlur(event: Event){
    if(this.kernel == null) this.kernel = 1;
    if(this.sigma == null) this.sigma = 1;
  }

  actualFiler(event: DropdownChangeEvent) {
    if (this.selectedFilter === null) {
      this.canUpload = false;
      return
    }
    else{
      this.selectedFilter?.name == 'Median' ? this.isMedian = true : this.isMedian = false;
      this.canUpload = true;
      this.selectedFilter = {
        name: event.value.name,
      };
    }
  }

  loadImageSrcOut(image: ImagesSrcOut) {
    this.imageSrcOut = image;
  }

  loadImageConvIn(image: IndexedImages) {
    this.imageConvIn = image;
  }

  loadIsLoading(isLoading: boolean) {
    this.isLoading = isLoading;
  }

}
