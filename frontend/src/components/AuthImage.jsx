/**
 * Composant pour afficher des images nécessitant une authentification
 */

import React, { useState, useEffect } from 'react';
import { FiImage } from 'react-icons/fi';
import authService from '../services/authService';

const AuthImage = ({ src, alt, className, onError }) => {
  const [imageSrc, setImageSrc] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const loadImage = async () => {
      try {
        const token = authService.getToken();
        
        const response = await fetch(src, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error('Failed to load image');
        }

        const blob = await response.blob();
        const objectUrl = URL.createObjectURL(blob);
        setImageSrc(objectUrl);
        setIsLoading(false);
      } catch (err) {
        console.error('Error loading image:', err);
        setError(true);
        setIsLoading(false);
        if (onError) onError(err);
      }
    };

    loadImage();

    // Cleanup: libérer l'URL de l'objet
    return () => {
      if (imageSrc) {
        URL.revokeObjectURL(imageSrc);
      }
    };
  }, [src]);

  if (isLoading) {
    return (
      <div className={`${className} flex items-center justify-center bg-gray-100`}>
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error || !imageSrc) {
    return (
      <div className={`${className} flex items-center justify-center bg-gray-100`}>
        <FiImage className="text-3xl text-gray-400" />
      </div>
    );
  }

  return <img src={imageSrc} alt={alt} className={className} />;
};

export default AuthImage;
