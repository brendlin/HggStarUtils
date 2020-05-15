
Double_t dscb(Double_t *x, Double_t *par)
{
  Float_t m =x[0];
  //Double_t f = TMath::Abs(par[0]*sin(par[1]*xx)/xx);

  Double_t norm = par[0];
  Double_t sigma = par[1];

  Double_t m0 = par[6];
  Double_t t = (m - m0) / sigma;

  Double_t alphaLo = par[2];
  Double_t alphaHi = par[3];
  
  Double_t nLo = par[4];
  Double_t nHi = par[5];

//   return 0.05*m;

  if (t < -alphaLo) {
    Double_t a = exp(-0.5 * alphaLo * alphaLo);
    Double_t b = nLo / alphaLo - alphaLo;
    //std::cout << a << " " << b << " " << nLo << " " << alphaLo << " " << std::endl;
    //std::cout << norm * a / pow(alphaLo / nLo * (b - t), nLo) << std::endl;
    return norm * a / pow(alphaLo / nLo * (b - t), nLo);
  }
  else if (t > alphaHi) {
    Double_t a = exp(-0.5 * alphaHi * alphaHi);
    Double_t b = nHi / alphaHi - alphaHi;
    return norm * a / pow(alphaHi / nHi * (b + t), nHi);
  }

  return norm * exp(-0.5 * t * t);  
}

